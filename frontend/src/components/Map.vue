<template>
  <div style="width: 100%; height: 100%; z-index: 0;" id="map"></div>
</template>

<script>
import eindhovenData from "../assets/EindhovenNeigh.json";
import utrechtData from "../assets/UtrechtNeigh.json";
import axios from "axios";

export default {
  computed: {
    calls() {
      return this.$store.getters.getCalls;
    },
    cbsData() {
      return this.$store.getter.getCbs;
    }
  },
  data() {
    return {
      center: [51.4416, 5.4697],
      zoom: 13,
      map: null,
      layers: [],
      titleLayer: null
    };
  },
  watch: {
    calls(newCalls, oldCalls) {
      this.setHeatMap();
    }
  },
  methods: {
    setHeatMap() {
      let allNewCalls = [
        {
          type: "ambulance",
          gradient: { 0.4: "#dbe900", 0.65: "#e37500", 1: "#b12c00" }
        },
        {
          type: "police",
          gradient: { 0.4: "#2aff50", 0.65: "#00c1d0", 1: "#559dff" }
        },
        {
          type: "fire-brigade",
          gradient: { 0.4: "#2e00bf", 0.65: "#8815ff", 1: "#ef00ff" }
        },
        {
          type: "helicopter",
          gradient: { 0.4: "#ff8cc6", 0.65: "#ffac81", 1: "#de369d" }
        }
      ];
      allNewCalls.forEach(call => {
        let newCalls = this.calls.filter(callType => {
          return callType.service === call.type;
        });

        let layer = this.layers.find(
          layer => layer.id === "heatmap-" + call.type
        );

        if (layer !== undefined) {
          layer.removeFrom(this.map);
          this.layers.splice(this.layers.indexOf(layer), 1);
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
    initLayers() {
      this.layers.forEach(layer => {
        const markerFeatures = layer.features.filter(
          feature => feature.type === "marker"
        );
        const polygonFeatures = layer.features.filter(
          feature => feature.type === "polygon"
        );

        markerFeatures.forEach(feature => {
          feature.leafletObject = L.marker(feature.coords).bindPopup(
            feature.name
          );
        });

        polygonFeatures.forEach(feature => {
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
      // this.layerChanged("UtrechtNeigh", true);
    },
    initMap() {
      this.map = L.map("map").setView(this.center, this.zoom);
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
        dataString += `<li>${this.$store.getters.getCbsKey[prop]}: ${data[prop]}</li>`;
      }
      dataString += "</ul>";
      return dataString;
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
  }
};
</script>

<style>
</style>
