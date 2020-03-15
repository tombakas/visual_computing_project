<template>
  <div class="info">
      <h6>Events in this period:</h6>
      <ul>
          <li v-for="(event, index) in events" :key="index">{{ event.name }}</li>
      </ul>
  </div>
</template>

<script>
export default {
    computed: {
        events() {
            return this.$store.getters.getEvents;
        }
    }, mounted() {
        this.$store.dispatch('getEvents', '', '')
    }
}
</script>

<style lang="scss">
@import '../scss/variables';
.info {
    position: absolute;
    background: map-get($map: $colors, $key: 'primary');
    top: 5px;
    right: 5px;
    height: 80px;
    max-width: calc(15% - 40px);
    color: map-get($map: $colors, $key: 'white');
    padding: 10px 20px;

    ul {
        list-style: disc inside none;
    }
}
</style>