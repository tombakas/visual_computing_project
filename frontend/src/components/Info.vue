<template>
  <div class="info">
    <h6>Events in this period:</h6>
    <ul>
      <li v-for="(event, index) in events" :key="index">{{ event.name }} at {{event.location}}</li>
    </ul>
  </div>
</template>

<script>
export default {
  computed: {
    events() {
      const size = this.$store.getters.getEvents.length;
      if (size === 0) {
        return [{name: 'No events', location: "this time period"}]
      } else if (size > 10 && size < 16) {
        return this.$store.getters.getEvents;
      } else {
        return this.$store.getters.getEvents.slice(0, 10);
      }
    }
  },
  mounted() {
    this.$store.dispatch("getEvents");
  }
};
</script>

<style lang="scss">
@import "../scss/variables";
.info {
  position: absolute;
  background: map-get($map: $colors, $key: "primary");
  top: 5px;
  right: 5px;
  max-width: calc(30% - 40px);
  color: map-get($map: $colors, $key: "white");
  padding: 10px 20px;

  ul {
    list-style: disc inside none;
  }
}
</style>