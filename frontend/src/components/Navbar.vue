<template>
  <nav>
    <h1>EmergenVis</h1>
    <div class="navigation-controls">
      <router-link class="mapButton" :to="{name: 'Map'}" v-on:click.native="loadCbsAttributes()">
        <img src="map.svg" alt />
        Map
      </router-link>
      <router-link
        class="graphsButton"
        :to="{name: 'Graphs'}"
        v-on:click.native="loadCbsAttributes()"
      >
        <img src="graph.svg" alt />
        Graphs
      </router-link>
    </div>
    <h5>Dispatch calls</h5>
    <div
      v-for="(value, key) in dispatchType"
      v-bind:key="'dispatch-' + key"
      class="dispatch-calls-control"
    >
      <input
        type="checkbox"
        :name="value.type"
        :id="key"
        v-model="value.checked"
        v-on:change="reloadData()"
      />
      <label
        :for="key"
        style=" -webkit-background-clip: text; margin-left: 10px"
      >{{ value.type.replace(/([A-Z])/g, ' $1').replace(/^./, function(str){ return str.toUpperCase(); }) }}</label>
      <div
        class="service-gradient-block"
        :style="{backgroundImage: 'linear-gradient(to right,' + value.colors + ')'}"
      ></div>
    </div>

    <b-button
      v-b-toggle.neighborhood-collapse
      @click="neighborhoodCollapsed=!neighborhoodCollapsed"
      class="neighborhood-toggle"
    >
      <h5>
        Neighborhood
        <span v-if="!neighborhoodCollapsed">></span>
        <span v-if="neighborhoodCollapsed">▼</span>
      </h5>
    </b-button>
    <b-collapse id="neighborhood-collapse">
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
          style="margin: 2px 10px"
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
    <h5>Display options</h5>
    <div>
      <input
        type="checkbox"
        :checked="displayPoints"
        v-on:click="changeDisplayPoints"
        id="displayPoints"
      />
      <label for="displayPoints" style="margin: 10px">Display points only</label>
    </div>
    <label style="margin-right: 10px">City</label>
    <select v-model="selectedCity">
      <option :value="city.name" v-for="(city, index) in getCity" :key="index">{{city.name}}</option>
    </select>
  </nav>
</template>

<script>
import axios from "axios";
import constants from "../constants.js";

export default {
  computed: {
    getCity() {
      return this.$store.getters.getCities;
    },
    displayPoints() {
      return this.$store.getters.getPoints;
    },
    getTimePeriod() {
      return this.$store.getters.getTimePeriod;
    }
  },
  data() {
    return {
      dispatchType: [
        {
          type: "police",
          checked: false,
          colors: constants.POLICE_COLORS.join(",")
        },
        {
          type: "ambulance",
          checked: false,
          colors: constants.AMBULANCE_COLORS.join(",")
        },
        {
          type: "fireBrigade",
          checked: false,
          colors: constants.FIRE_BRIGADE_COLORS.join(",")
        },
        {
          type: "helicopter",
          checked: false,
          colors: constants.HELICOPTER_COLORS.join(",")
        }
      ],
      neighborhood: [],
      timePeriod: {
        from: null,
        to: new Date().toISOString().split("T")[0],
      },
      limit: 5000,
      cities: ["Eindhoven", "Utrecht"],
      selectedCity: "Eindhoven",
      neighborhoodCollapsed: false
    };
  },
  watch: {
    selectedCity(newCity, oldCity) {
      this.$store.dispatch("setCity", newCity);
      this.$store.dispatch("getEvents");
    },
    getTimePeriod(newTime, oldTime) {
      this.timePeriod.from = newTime.from;
      this.timePeriod.to = newTime.to;
    }
  },
  methods: {
    changeDisplayPoints() {
      this.$store.dispatch("setDisplayPoints", this.displayPoints);
    },
    reloadData() {
      let params = {
        limit: this.limit,
        to: this.timePeriod.to
      };

      this.$store.dispatch("setTimePeriod", this.timePeriod);

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
      this.$store.dispatch("getEvents");
    },
    loadCbsAttributes() {
      this.neighborhood = [];
      axios
        .get("http://localhost:5000/api/cbs?region=Binnenstad")
        .then(result => {
          for (let attr in result.data[0]) {
            if (attr.indexOf("_cat") > -1) {
              if (this.$route.name === "Graphs") {
                let originalKey = attr.substring(0, attr.indexOf("_cat"));
                this.neighborhood.push({
                  type:
                    this.$store.getters.getCbsKey[originalKey] + " categorized",
                  key: attr,
                  checked: false
                });
              } else {
                continue;
              }
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
    }
  },
  mounted() {
    this.reloadData();
    this.loadCbsAttributes();
  }
};
</script>

<style scoped>
.navigation-controls {
  display: flex;
  justify-content: space-evenly;
  margin: -10px 0 20px 0;
  padding: 20px 0;
}

.mapButton,
.graphsButton {
  width: 50px;
  height: 50px;
  text-align: center;
  color: white;
  outline: none;

  opacity: 0.7;
}

.mapButton:hover {
  opacity: 1;
  text-decoration: none;
}

.graphsButton:hover {
  opacity: 1;
  text-decoration: none;
}
</style>
