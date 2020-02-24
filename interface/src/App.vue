<template>
  <div id="app">
    <navigation></navigation>
    <base-map></base-map>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import BaseMap from './components/Map';
import Navigation from './components/Navbar';

export default {
  name: 'App',
  components: {
    BaseMap, Navigation
  }
}
</script>

<style lang="scss">

</style>
