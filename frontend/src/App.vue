<template>
  <div id="app">
    <navigation></navigation>
    <base-map></base-map>
    <time-bar></time-bar>
    <info></info>
  </div>
</template>

<script>
import Info from "./components/Info";
import BaseMap from "./components/Map";
import TimeBar from "./components/TimeBar";
import Navigation from "./components/Navbar";

export default {
  name: "App",
  components: {
    Info,
    BaseMap,
    TimeBar,
    Navigation
  }
};
</script>

<style lang="scss">
@import "./scss/app.scss";
</style>
