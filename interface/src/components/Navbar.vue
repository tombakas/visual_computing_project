<template>
  <nav><h1>App name</h1></nav>
</template>

<script>
export default {

}
</script>

<style lang="scss">
@import '../scss/variables';

nav {
    background-color: map-get($map: $colors, $key: 'black');
    color: map-get($map: $colors, $key: 'white');
    width: 20%;
    height: 100%;
    left: 0;
    overflow-y: auto;
    padding: 10px 20px;
}
</style>