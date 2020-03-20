<template>
  <div style="width: 100%; height: 100%;">
    <MglMap :accessToken="accessToken" :mapStyle="mapStyle" :center="center" :zoom="zoom">
      <MglGeojsonLayer
        :sourceId="eindhovenData.data.id"
        :source="eindhovenData"
        layerId="tileLayer"
        :layer="tileLayer"
      />
       <!-- <MglGeojsonLayer
        :sourceId="utrechtData.data.id"
        :source="utrechtData"
        layerId="tileLayer"
        :layer="tileLayer"
      />  -->
      <MglGeojsonLayer
        :sourceId="calls.data.id"
        :source="calls"
        layerId="Test"
        :layer="geoJsonLayer"
      />  
    </MglMap>
  </div>
</template>

<script>
import Mapbox from "mapbox-gl";
import { MglMap, MglGeojsonLayer, MglPopUP } from "vue-mapbox";


import eindhovenData from "../assets/EindhovenNeigh.json";
import utrechtData from "../assets/UtrechtNeigh.json";

export default {
  components: {
    MglMap,
    MglGeojsonLayer,
  },
  computed: {
    calls() {
      return this.$store.getters.getCalls;
    }
  },
  data() {
    return {
      eindhovenData: eindhovenData,
      utrechtData: utrechtData,
      accessToken:
        "pk.eyJ1IjoiY2h1cnJvcyIsImEiOiJjazZxdHlkNWQwMGViM21wZHMzMWRxazBvIn0.tdWPYNbC-n38mpRA23WFyQ",
      mapStyle: "mapbox://styles/mapbox/streets-v11",
      center: [5.4697, 51.4416],
      zoom: 11.5,
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
      geoJsonLayer: {
        type: "heatmap",
        paint: {
          // Increase the heatmap weight based on frequency and property magnitude
          "heatmap-weight": [
            "interpolate",
            ["linear"],
            ["get", "mag"],
            0,
            0,
            6,
            1
          ],
          // Increase the heatmap color weight weight by zoom level
          // heatmap-intensity is a multiplier on top of heatmap-weight
          "heatmap-intensity": [
            "interpolate",
            ["linear"],
            ["zoom"],
            0,
            1,
            9,
            3
          ],
          // Color ramp for heatmap.  Domain is 0 (low) to 1 (high).
          // Begin color ramp at 0-stop with a 0-transparancy color
          // to create a blur-like effect.
          "heatmap-color": [
            "interpolate",
            ["linear"],
            ["heatmap-density"],
            0,
            "rgba(33,102,172,0)",
            0.2,
            "rgb(103,169,207)",
            0.4,
            "rgb(209,229,240)",
            0.6,
            "rgb(253,219,199)",
            0.8,
            "rgb(239,138,98)",
            1,
            "rgb(178,24,43)"
          ],
          // Adjust the heatmap radius by zoom level
          "heatmap-radius": ["interpolate", ["linear"], ["zoom"], 0, 2, 9, 10],
          // Transition from heatmap to circle layer by zoom level
          "heatmap-opacity": ["interpolate", ["linear"], ["zoom"], 11, 1, 19, 3]
        }
      }
    };
  },
  created() {
    this.mapbox = Mapbox;
  }
};
</script>

<style>
</style>
