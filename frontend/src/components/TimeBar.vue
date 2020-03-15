<template>
  <div class="timebar">
    <span>play button</span>
  </div>
</template>

<script>
export default {};
</script>

<style lang="scss">
@import '../scss/variables';

.timebar {
  width: 80%;
  position: absolute;
  right: 0;
  bottom: 0;
  height: 100px;
  background: rgba($color: (map-get($map: $colors , $key: 'black')), $alpha: 0.4);
  z-index: 2;
}
</style>