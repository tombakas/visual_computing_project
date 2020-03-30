<template>
  <div id="app">
    <navigation></navigation>
    <router-view></router-view>
  </div>
</template>

<script>
import Navigation from "./components/Navbar";

export default {
  name: "App",
  components: {
    Navigation
  }
};
</script>

<style lang="scss">
@import "./scss/app.scss";
</style>
