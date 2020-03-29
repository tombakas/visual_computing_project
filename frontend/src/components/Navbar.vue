<template>
  <nav>
    <h1>App name</h1>
    <h5>Dispatch calls</h5>
    <div v-for="(value, key) in dispatchType" v-bind:key="'dispatch-' + key" class="dispatch-calls-control">
      <input
        type="checkbox"
        :name="value.type"
        :id="key"
        v-model="value.checked"
        v-on:change="reloadData()"
      />
      <label
        :for="key"
        style=" -webkit-background-clip: text"
      >{{ value.type.replace(/([A-Z])/g, ' $1').replace(/^./, function(str){ return str.toUpperCase(); }) }}</label>
      <div
        class="service-gradient-block"
        :style="{backgroundImage: 'linear-gradient(to right,' + value.colors + ')'}"
        >
      </div>
    </div>
   
      <b-button v-b-toggle.neighborhood-collapse @click="neighborhoodCollapsed=!neighborhoodCollapsed" class="neighborhood-toggle">
        <h5>
          Neighborhood
          <span v-if="!neighborhoodCollapsed">⯈</span>
          <span v-if="neighborhoodCollapsed" >▼</span>
        </h5>
      </b-button>
      <b-collapse id="neighborhood-collapse" >
        <div v-for="(value, key) in neighborhood" v-bind:key="'neighborhood-' + key">
          <input
            type="checkbox"
            :name="value.type"
            :id="key"
            v-model="value.checked"
            v-on:change="setAttribute(value.key)"
            />
          <label
            :for="key"
            >{{ value.type.replace(/([A-Z])/g, ' $1').replace(/^./, function(str){ return str.toUpperCase(); }) }}</label>
        </div>
    </b-collapse>
    <h5>Time period</h5>
    <div class="time-period-toggle">
      <div>
        <label for="fromDate">From</label>
        <input type="date" v-model="timePeriod.from" v-on:change="reloadData()" />
      </div>
      <div>
        <label for="fromDate">To</label>
        <input type="date" v-model="timePeriod.to" v-on:change="reloadData()" />
      </div>
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
    <select v-model="selectedCity">
      <option :value="city.name" v-for="(city, index) in getCity" :key="index" >{{city.name}}</option>
    </select>
  </nav>
</template>

<script>
import axios from "axios";

export default {
  computed: {
    getCity(){
      return this.$store.getters.getCities;
    }
  },
  data() {
    return {
      dispatchType: [
        { type: "police", 
          checked: false, 
          colors: "#dbe900, #e37500, #b12c00" },
        {
          type: "ambulance",
          checked: false,
          colors: "#2aff50, #00c1d0, #559dff"
        },
        {
          type: "fireBrigade",
          checked: false,
          colors: "#2e00bf, #8815ff, #ef00ff"
        },
        {
          type: "helicopter",
          checked: false,
          colors: "#ff8cc6, #ffac81 , #de369d"
        }
      ],
      neighborhood: [],
      timePeriod: {
        from: null,
        to: new Date().toISOString().split("T")[0]
      },
      limit: 100,
      cities: ["Eindhoven", "Utrecht"],
      selectedCity: "Eindhoven",
      neighborhoodCollapsed: false
    };
  },
  watch: {
    selectedCity(newCity, oldCity){
      this.$store.dispatch("setCity", newCity);
    }
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
          if (type !== "") {
            type += ",";
          }
          type += service.type;
        }
      });
      params.service = type;
      this.$store.dispatch("getCalls", params);
    },
    loadCbsAttributes() {
      axios
        .get("http://localhost:5000/api/cbs?region=Binnenstad")
        .then(result => {
          for (let attr in result.data[0]) {
            if (attr.indexOf("_cat") > -1) {
              let orignalKey = attr.substring(0, attr.indexOf("_cat"));
              this.neighborhood.push({
                type:
                  this.$store.getters.getCbsKey[orignalKey] + " categorized",
                key: attr,
                checked: false
              });
            } else {
              this.neighborhood.push({
                type: this.$store.getters.getCbsKey[attr],
                key: attr,

                checked: false
              });
            }
          }
        });
    },
    setAttribute(attribute) {
      this.$store.dispatch("setAttribute", attribute);
    },
  },
  mounted() {
    this.reloadData();
    this.loadCbsAttributes();
  }
};
</script>
