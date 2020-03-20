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
    <h5>Number of incidents</h5>
    <input type="range" name="limit" id="limit" min="100" max="100000" v-on:change="reloadData()" v-model="limit" step="100">
    <label for="limit">{{ limit }} incidents</label>
    <h5>City</h5>
    <select name="" id="">
      <option value="city" v-for="(city, index) in cities" :key="index">{{city}}</option>
    </select>
    
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
      },
      limit: 1000,
      cities: ['Eindhoven', 'Utrecht']
    };
  },
  methods: {
    reloadData(){
      let params = {
        'limit' : this.limit,
      }
      this.$store.dispatch('getCalls', params);
    }
  },
  mounted() {
    this.reloadData();
  }
};
</script>
