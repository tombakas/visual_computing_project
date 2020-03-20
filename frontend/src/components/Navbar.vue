<template>
  <nav>
    <h1>App name</h1>
    <h5>Dispatch calls</h5>
    <div v-for="(value, key) in dispatchType" v-bind:key="'dispatch-' + key">
      <input
        type="checkbox"
        :name="value.type"
        :id="key"
        v-model="value.checked"
        v-on:change="reloadData()"
      />
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
      <input type="date" v-model="timePeriod.from" v-on:change="reloadData()" />
    </div>
    <div>
      <label for="fromDate">To</label>
      <input type="date" v-model="timePeriod.to" v-on:change="reloadData()" />
    </div>
    <h5>Number of incidents</h5>
    <input
      type="range"
      name="limit"
      id="limit"
      min="100"
      max="50000"
      v-on:change="reloadData()"
      v-model="limit"
      step="100"
    />
    <label for="limit">{{ limit }} incidents</label>
    <h5>City</h5>
    <select name id>
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
        { type: "ambulance", checked: true },
        { type: "fireBrigade", checked: false }
      ],
      neighborhood: [
        { type: "averageIncome", checked: false },
        { type: "crimeRates", checked: false }
      ],
      timePeriod: {
        from: null,
        to: new Date().toISOString().split("T")[0]
      },
      limit: 1000,
      cities: ["Eindhoven", "Utrecht"]
    };
  },
  methods: {
    reloadData() {
      let params = {
        limit: this.limit,
        to: this.timePeriod.to
      };

      if (this.timePeriod.from !== null) {
        params.from = this.timePeriod.from;
      }

      let type = "";
      this.dispatchType.forEach(service => {
        if (service.checked) {
          type += service.type + ",";
        }
      });
      params.type = type;
      this.$store.dispatch("getCalls", params);
    }
  },
  mounted() {
    this.reloadData();
  }
};
</script>
