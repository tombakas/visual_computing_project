<template>
  <div style="width: 100%; height: 100%; z-index: 0;" id="map"></div>
</template>

<script>
import eindhovenData from "../assets/EindhovenNeigh.json";
import utrechtData from "../assets/UtrechtNeigh.json";
import constants from "../constants.js";
import axios from "axios";

export default {
  computed: {
    calls() {
      return this.$store.getters.getCalls;
    },
    cbsAttributes() {
      return this.$store.getters.getCbsAttributes;
    },
    currentCity() {
      return this.$store.getters.getCity;
    },
    displayPoints() {
      return this.$store.getters.getPoints;
    }
  },
  data() {
    return {
      center: [51.4416, 5.4697],
      zoom: 12,
      map: null,
      layers: [],
      titleLayer: null
    };
  },
  watch: {
    calls(newCalls, oldCalls) {
      this.visualizeCalls(true);
    },
    cbsAttributes(newData, oldData) {
      this.setCbsPopup();
    },
    currentCity(newCity, oldCity) {
      this.panToCity(newCity);
    },
    displayPoints(newValue, oldValue) {
      this.visualizeCalls(true);
    }
  },
  methods: {
    visualizeCalls(dataChanged) {
      if (
        ((this.map.getZoom() <= 15 && dataChanged) ||
        (this.map.getZoom() <= 15 && this.zoom > 15)) && !this.displayPoints
      ) {
        this.setHeatMap(dataChanged);
      } else if (
        (this.map.getZoom() > 15 && dataChanged) ||
        (this.map.getZoom() > 15 && this.zoom <= 15) ||
        this.displayPoints
      ) {
        this.setCluster(dataChanged);
      }
      this.zoom = this.map.getZoom();
    },
    setCluster(dataChanged) {
      let allCallTypes = ["ambulance", "police", "fire-brigade", "helicopter"];

      allCallTypes.forEach(callType => {
        let layer = this.layers.find(
          layer => layer.id === "heatmap-" + callType
        );

        if (layer !== undefined) {
          layer.removeFrom(this.map);
          this.layers.splice(this.layers.indexOf(layer), 1);
        }
      });

      if (dataChanged) {
        let layer = this.layers.find(layer => layer.id === "clustered");

        if (layer !== undefined) {
          layer.removeFrom(this.map);
          this.layers.splice(this.layers.indexOf(layer), 1);
        }
      }

      let markers = L.markerClusterGroup();
      markers.id = "clustered";
      this.calls.forEach(call => {
        let marker = L.marker(call.coords, { title: call.service });
        marker.bindPopup(call.service);
        markers.addLayer(marker);
      });

      this.layers.push(markers);
      markers.addTo(this.map);
    },
    setHeatMap(dataChanged) {
      let layer = this.layers.find(layer => layer.id === "clustered");

      if (layer !== undefined) {
        layer.removeFrom(this.map);
        this.layers.splice(this.layers.indexOf(layer), 1);
      }

      let allNewCalls = [
        {
          type: "ambulance",
          gradient: {
            0.4: constants.AMBULANCE_COLORS[0],
            0.65: constants.AMBULANCE_COLORS[1],
            1: constants.AMBULANCE_COLORS[2]
          }
        },
        {
          type: "police",
          gradient: {
            0.4: constants.POLICE_COLORS[0],
            0.65: constants.POLICE_COLORS[1],
            1: constants.POLICE_COLORS[2]
          }
        },
        {
          type: "fire-brigade",
          gradient: {
            0.4: constants.FIRE_BRIGADE_COLORS[0],
            0.65: constants.FIRE_BRIGADE_COLORS[1],
            1: constants.FIRE_BRIGADE_COLORS[2]
          }
        },
        {
          type: "helicopter",
          gradient: {
            0.4: constants.HELICOPTER_COLORS[0],
            0.65: constants.HELICOPTER_COLORS[1],
            1: constants.HELICOPTER_COLORS[2]
          }
        }
      ];
      allNewCalls.forEach(call => {
        let newCalls = this.calls.filter(callType => {
          return callType.service === call.type;
        });

        if (dataChanged) {
          let layer = this.layers.find(
            layer => layer.id === "heatmap-" + call.type
          );

          if (layer !== undefined) {
            layer.removeFrom(this.map);
            this.layers.splice(this.layers.indexOf(layer), 1);
          }
        }

        let incidentCoords = [];
        newCalls.forEach(call => {
          incidentCoords.push(call.coords);
        });

        layer = L.heatLayer(incidentCoords, { gradient: call.gradient });
        layer.id = "heatmap-" + call.type;
        this.layers.push(layer);
        layer.addTo(this.map);
      });
    },
    convertNeighborhoods(neighborhoodData, city, id) {
      let cityData = {
        id: id,
        name: city,
        active: false,
        features: []
      };

      neighborhoodData.data.features.forEach(neighborhood => {
        let neighborhoodGeo = {
          name: neighborhood.properties.nameNeigh,
          type: "polygon",
          coords: neighborhood.geometry.coordinates
        };
        cityData.features.push(neighborhoodGeo);
      });
      return cityData;
    },
    layerChanged(layerId, active) {
      const layer = this.layers.find(layer => layer.id === layerId);
      layer.features.forEach(feature => {
        if (active) {
          feature.leafletObject.addTo(this.map);
        } else {
          feature.leafletObject.removeFrom(this.map);
        }
      });
    },
    setCbsPopup() {
      this.layers.forEach(layer => {
        if (Array.isArray(layer)) {
          return;
        }

        if (layer.features === undefined) {
          return;
        }

        this.layerChanged("EindhovenNeigh", false);
        this.layerChanged("UtrechtNeigh", false);

        const polygonFeatures = layer.features.filter(
          feature => feature.type === "polygon"
        );

        polygonFeatures.forEach(feature => {
          feature.name = feature.name.replace(/(\,|\')/g, "");
          let requestParams = "?region=" + feature.name;
          if (this.cbsAttributes.length > 0) {
            requestParams += "&columns=";
            this.cbsAttributes.forEach(attribute => {
              if (requestParams.slice(requestParams.length - 1) !== "=") {
                requestParams += ",";
              }
              requestParams += attribute;
            });
          }
          axios
            .get("http://localhost:5000/api/cbs" + requestParams)
            .then(result => {
              feature.leafletObject.unbindPopup();
              feature.leafletObject.bindPopup(
                this.setNeighborhoodProps(result.data[0])
              );
            })
            .catch(error => {
              console.error(feature.name, error);
            });

          feature.leafletObject = L.polygon(feature.coords, {
            color: "#c2c0c0"
          });
        });
      });

      this.layerChanged("EindhovenNeigh", true);
      this.layerChanged("UtrechtNeigh", true);
    },
    initLayers() {
      this.layers.forEach(layer => {
        const polygonFeatures = layer.features.filter(
          feature => feature.type === "polygon"
        );

        polygonFeatures.forEach(feature => {
          feature.name = feature.name.replace(/(\,|\')/g, "");
          let requestParams = "?region=" + feature.name;
          if (this.cbsAttributes.length > 0) {
            this.requestParams.forEach(attribute => {
              if (requestParams.indexOf("=") !== -1) {
                requestParams += ",";
              }
              requestParams += attribute;
            });
          }
          axios
            .get("http://localhost:5000/api/cbs?region=" + feature.name)
            .then(result => {
              feature.leafletObject.bindPopup(
                this.setNeighborhoodProps(result.data[0])
              );
            })
            .catch(error => {
              console.error(feature.name, error);
            });

          feature.leafletObject = L.polygon(feature.coords, {
            color: "#c2c0c0"
          });
        });
      });

      this.layerChanged("EindhovenNeigh", true);
      this.layerChanged("UtrechtNeigh", true);
    },
    initMap() {
      this.map = L.map("map").setView(
        this.$store.getters.getCity.center,
        this.zoom
      );
      this.tileLayer = L.tileLayer(
        "https://cartodb-basemaps-{s}.global.ssl.fastly.net/rastertiles/voyager/{z}/{x}/{y}.png",
        {
          maxZoom: 18,
          attribution:
            '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attribution">CARTO</a>'
        }
      );

      this.tileLayer.addTo(this.map);
    },
    setNeighborhoodProps(data) {
      let dataString = "<ul>";
      for (const prop in data) {
        if (prop.indexOf("_cat") > -1) {
          continue;
        } else {
          dataString += `<li>${this.$store.getters.getCbsKey[prop]}: ${data[prop]}</li>`;
        }
      }
      dataString += "</ul>";
      return dataString;
    },
    panToCity(city) {
      this.map.flyTo(this.$store.getters.getCity.center, this.zoom);
    }
  },
  mounted() {
    this.layers.push(
      this.convertNeighborhoods(eindhovenData, "Eindhoven", "EindhovenNeigh")
    );
    this.layers.push(
      this.convertNeighborhoods(utrechtData, "Utrecht", "UtrechtNeigh")
    );
    this.initMap();
    this.initLayers();

    let that = this;
    this.map.on("zoomend", function() {
      that.visualizeCalls(false);
    });
  }
};
</script>

<style>
</style>
