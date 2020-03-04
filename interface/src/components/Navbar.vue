<template>
  <nav>
    <h1>App name</h1>
    <h5>Dispatch calls</h5>
    <div v-for="(value, key) in dispatchType" v-bind:key="'dispatch-' + key">
      <input type="checkbox" :name="value.type" :id="key" v-model="value.checked" />
      <label
        :for="key"
      >{{ value.type.replace(/([A-Z])/g, ' $1').replace(/^./, function(str){ return str.toUpperCase(); }) }}</label>
    </div>
    <h5>Neighborhood</h5>
    <div v-for="(value, key) in neighborhood" v-bind:key="'neighborhood-' + key">
      <input type="checkbox" :name="value.type" :id="key" v-model="value.checked" />
      <label
        :for="key"
      >{{ value.type.replace(/([A-Z])/g, ' $1').replace(/^./, function(str){ return str.toUpperCase(); }) }}</label>
    </div>
    <h5>Time period</h5>
    <div>
      <label for="fromDate">From</label>
      <input type="datetime-local" name id />
    </div>
    <div>
      <label for="fromDate">To</label>
      <input type="datetime-local" name id />
    </div>
  </nav>
</template>

<script>
export default {
  computed: {},
  data() {
    return {
      dispatchType: [
        { type: "police", checked: false },
        { type: "ambulance", checked: false },
        { type: "fireBrigade", checked: false }
      ],
      neighborhood: [
        { type: "averageIncome", checked: false },
        { type: "crimeRates", checked: false }
      ],
      timePeriod: {
        from: "",
        to: ""
      }
    };
  },
  mounted() {
    this.$store.dispatch("getLatest");
  }
};
</script>
