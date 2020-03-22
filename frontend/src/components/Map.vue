<template>
  <div style="width: 100%; height: 100%;" id="map"></div>
</template>

<script>
import Mapbox from "mapbox-gl";
import { MglMap, MglGeojsonLayer, MglPopUP } from "vue-mapbox";

import eindhovenData from "../assets/EindhovenNeigh.json";
import utrechtData from "../assets/UtrechtNeigh.json";

export default {
  components: {
    MglMap,
    MglGeojsonLayer
  },
  computed: {
    calls() {
      
      return this.$store.getters.getCalls;
    },
  },
  data() {
    return {

      accessToken:
        "pk.eyJ1IjoiY2h1cnJvcyIsImEiOiJjazZxdHlkNWQwMGViM21wZHMzMWRxazBvIn0.tdWPYNbC-n38mpRA23WFyQ",
      mapStyle: "mapbox://styles/mapbox/streets-v11",
      center: [51.4416, 5.4697],
      zoom: 13,
      tileLayer: {
        id: "tileLayer",
        type: "fill",
        layout: {},
        paint: {
          "fill-color": "#088",
          "fill-opacity": 0.8,
          "fill-outline-color": "#000000"
        }
      },
      map: null,
      layers: [],
      titleLayer: null,
    };
  },
  created() {
    this.mapbox = Mapbox;
  },
  methods: {
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
          feature.leafletObject = L.polygon(feature.coords).bindPopup(
            feature.name
          );
        });
      });

      this.layerChanged(0, true);
      // this.layerChanged(3, true)
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
    }
  },
  mounted() {
    this.layers.push(this.convertNeighborhoods(eindhovenData, "Eindhoven", 0));
    // this.layers.push(this.convertNeighborhoods(utrechtData, "Utrecht", 3));
    this.initMap();
    this.initLayers();    
 }
};
</script>

<style>
</style>
