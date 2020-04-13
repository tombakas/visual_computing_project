<template>
  <div class="mapview">
    <leaflet-map></leaflet-map>
    <time-bar></time-bar>
    <info></info>
  </div>
</template>

<script>
import Info from "./Info";
import LeafletMap from "./Map";
import BaseMap from "./Map";
import TimeBar from "./TimeBar";

export default {
  components: {
    Info,
    BaseMap,
    TimeBar,
    LeafletMap
  }
};
</script>

<style>
.mapview {
    width: 100%;
    height: 100%;
}
</style>