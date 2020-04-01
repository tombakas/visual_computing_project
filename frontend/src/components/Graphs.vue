<template>
  <div class="graphs">
    <router-link :to="{name: 'bayesian'}" tag="div" class="graphs__item">Bayesian Network</router-link>
    <router-link :to="{name: 'parcorplot'}" tag="div" class="graphs__item">Parallel Coordinate Plot</router-link>
    <router-link :to="{name: 'scatplot'}" tag="div" class="graphs__item">Scatter plot</router-link>
  </div>
</template>

<script>
export default {};
</script>

<style lang="scss" scoped>
@import "../scss/_variables.scss";

.graphs {
  display: flex;
  align-items: center;
  justify-content: space-evenly;
  width: 100%;

  &__item {
    display: flex;
    align-items: flex-end;
    justify-content: flex-end;
    width: 25%;
    height: 30%;
    padding: 10px 15px;
    border-radius: 8px;
    transition-duration: 0.5s;
    color: map-get($map: $colors, $key: 'white');

    &:hover {
      box-shadow: 0px 0px 10px 2px rgba(0, 0, 0, 0.5);
    }

    &:first-of-type {
      background-color: map-get($map: $colors, $key: 'primary');
    }
    &:nth-of-type(2) {
      background-color: map-get($map: $colors, $key: 'secondary');
      color: map-get($map: $colors, $key: 'black')
    }

    &:nth-of-type(3) {
      background-color: map-get($map: $colors, $key: 'tertiary');
    }
  }
}
</style>