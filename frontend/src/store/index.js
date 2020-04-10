import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    displayedCalls: [],
    playbackDate: {},
    allCalls: [],
    timePeriod: {
      from: "",
      to: ""
    },
    dispatchType: {},
    neighborhoodData: {},
    events: [],
    city: 0,
    cities: [
      {
        name: "Eindhoven",
        center: [51.4416, 5.4697]
      },
      {
        name: "Utrecht",
        center: [52.0907, 5.1214]
      }
    ],
    cbsAttributes: [],
    cbsDataKey: {
      a_00_14: "Age 0-14",
      a_15_24: "Age 15-24",
      a_25_44: "Age 25-44",
      a_45_64: "Age 45-64",
      a_65_oo: "Age 65+",
      a_ao: "Disability allowance",
      a_aow: "Old age pension",
      a_bijstand: "Social security payments",
      a_car: "#cars",
      a_comp: "#companies",
      a_died: "#died",
      a_female: "#females",
      a_hh: "#households",
      a_house: "#houses",
      a_inc_rec: "#income recipients",
      a_inh: "#inhabitants",
      a_lan_ac: "Area in acres",
      a_male: "#males",
      a_nw_all: "#non-western persons",
      a_sur_ac: "Surface area in acres",
      a_w_all: "#western persons",
      a_wat_ac: "Water area in acres",
      a_ww: "#persons in unemployment security law",
      av_assault: "#assaults (avg)",
      av_car_hh: "#cars per household (avg)",
      av_des_po: "#destruction and public misbehavior (avg)",
      av_hh_size: "Average household size",
      av_hou_theft: "#theft in houses (avg)",
      av_inc_inh_x1000: "Income per 1000 (avg)",
      av_inc_rec_x1000: "Average income per income recipient x1000",
      av_km_dc: "Distance to daycare in km (avg)",
      av_km_doc: "Distance to gp in km (avg)",
      av_km_sc: "Distance to school in km (avg)",
      av_km_sup: "Distance to supermarket in km (avg)",
      av_prop_val_x1000: "Property value x1000 (avg)",
      city_name: "Name of city",
      p_hh_usm: "Percentage of households under social minimum",
      p_n_act: "Percentage of working people",
      per_build_af_2000: "Percentage houses built after 2000",
      per_build_be_2000: "Percentage houses built before 2000",
      per_own_occ: "Percentage occupied houses",
      per_ren_hou: "Percentage of rental houses",
      per_uninhab: "Percentage of houses uninhabited",
      pop_den_km2: "Population density per km2 ",
      region: "Neighborhood name"
    },
    abortPlayback: false
  },
  mutations: {
    SET_DATA(state, calls) {
      state.displayedCalls = calls;
    },
    SET_TIME_PERIOD(state, timePeriod) {
      state.timePeriod = timePeriod;
    },
    SET_EVENTS(state, events) {
      state.events = events;
    },
    SET_CBS(state, data) {
      state.neighborhoodData = data;
    },
    SET_CITY(state, city) {
      state.city = city;
    },
    SET_ATTRIBUTE(state, attribute) {
      if (state.cbsAttributes.indexOf(attribute) !== -1) {
        state.cbsAttributes = state.cbsAttributes.filter(attr => {
          return attr !== attribute;
        });
      } else {
        state.cbsAttributes.push(attribute);
      }
    },
    SET_PLAYBACK_DATE(state, date) {
      state.playbackDate = date;
    },
    SET_ALL_CALLS(state, calls) {
      state.allCalls = calls;
    },
    SET_ABORT_PLAYBACK(state, stopPlayback) {
      state.abortPlayback = stopPlayback;
    }
  },
  actions: {
    setTimePeriod({ commit }, timePeriod) {
      commit("SET_TIME_PERIOD", timePeriod);
    },
    getCalls({ commit }, params) {
      let requestParams = "?";
      for (let param in params) {
        requestParams += `${param}=${params[param]}&`;
      }
      axios
        .get("http://localhost:5000/api/calls/" + requestParams)
        .then(result => {
          result.data.forEach(call => {
            call.coords = L.latLng(call.lat, call.lon);
          });
          commit("SET_DATA", result.data);
        })
        .catch(error => {
          console.error(error);
        });
    },
    getPlaybackCalls({ commit, dispatch }, calls) {
      if (this.state.allCalls.length === 0) {
        let total = 0;
        let currentDay = new Date(calls[0].datetime);
        this.state.displayedCalls.forEach(call => {
          if (!datesSameDay(new Date(call.datetime), currentDay)){
            total++;
            currentDay = new Date(call.datetime);
          }
        });
        commit("SET_ALL_CALLS", this.state.displayedCalls);
        commit("SET_DATA", []);
        commit("SET_PLAYBACK_DATE", {
          date: new Date(calls[0].datetime),
          count: 0,
          total: total
        });
      }


      commit("SET_PLAYBACK_DATE", {
        date: new Date(calls[0].datetime),
        count: this.state.playbackDate.count + 1,
        total: this.state.playbackDate.total
      });
      let index = calls.findIndex(
        call => !datesSameDay(new Date(call.datetime), this.state.playbackDate.date)
      );

      commit("SET_DATA", calls.slice(0, index - 1));

      const that = this;
      setTimeout(function() {
        if (index !== -1 && !that.state.abortPlayback) {
          dispatch("getPlaybackCalls", calls.slice(index));
        } else {
          commit("SET_DATA", that.state.allCalls);
          commit("SET_ALL_CALLS", []);
          commit("SET_PLAYBACK_DATE", {});
          commit("SET_ABORT_PLAYBACK", false);
        }
      }, 1500);
    },
    getEvents({ commit }) {
      // TODO Set up endpoint on backend
      let searchQuery = "?city=" + this.state.cities[this.state.city].name;

      if (this.state.timePeriod.from !== "") {
        searchQuery += "&from=" + this.state.timePeriod.from;
      }

      if (this.state.timePeriod.to !== "") {
        searchQuery += "&to=" + this.state.timePeriod.to;
      }

      axios
        .get("http://localhost:5000/api/events" + searchQuery)
        .then(result => {
          commit("SET_EVENTS", result.data);
        })
        .catch(error => {
          console.error(error);
        });
    },
    setAttribute({ commit }, attribute) {
      commit("SET_ATTRIBUTE", attribute);
    },
    setCity({ commit }, city) {
      commit(
        "SET_CITY",
        this.state.cities.indexOf(
          this.state.cities.find(stateCity => {
            return city === stateCity.name;
          })
        )
      );
    },
    setPlayback({ commit }, stopPlayback) {
      commit("SET_ABORT_PLAYBACK", stopPlayback);
    }
  },
  getters: {
    getCity: state => state.cities[state.city],
    getCities: state => state.cities,
    getCalls: state => state.displayedCalls,
    getEvents: state => state.events,
    getCbs: state => state.neighborhoodData,
    getCbsKey: state => state.cbsDataKey,
    getCbsAttributes: state => state.cbsAttributes,
    getPlaybackDate: state => state.playbackDate,
    getAbortPlayback: state => state.abortPlayback
  }
});

const datesSameDay = (first, second) =>
  first.getFullYear() === second.getFullYear() &&
  first.getMonth() === second.getMonth();
// first.getDate() === second.getDate();
