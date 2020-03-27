import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    calls: {
      data: {
        id: "default"
      }
    },
    timePeriod: {
      from: "",
      to: ""
    },
    dispatchType: {},
    neighborhoodData: {},
    events: [],
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
    }
  },
  mutations: {
    SET_DATA(state, calls) {
      state.calls = calls;
    },
    SET_TIME_PERIOD(state, timePeriod) {
      state.timePeriod = timePeriod;
    },
    SET_EVENTS(state, events) {
      state.events = events;
    },
    SET_CBS(state, data) {
      state.neighborhoodData = data;
    }
  },
  actions: {
    setTimePeriod({ commit }, timePeriod) {
      commit("SET_TIME_PERIOD", timePeriod);
    },
    getLatest({ commit }) {
      axios
        .get("http://localhost:5000/api/calls/?limit=10000")
        .then(result => {
          commit("SET_DATA", coordToGeoJson(result.data, "latest"));
        })
        .catch(error => {});
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
    getCbsData({ commit }, params) {
      let requestParams = "?";
      requestParams += "region=" + params.neighborhood;
      if (params.columns !== undefined && params.columns.length > 0) {
        requestParams += "&columns=";
      }
      params.columns.forEach((column, index) => {
        if (index > 0) {
          requestParams += ",";
        }
        requestParams += column;
      });

      axios
        .get("http://localhost:5000/api/cbs" + requestParams)
        .then(result => {
          commit("SET_CBS", result.data);
        })
        .catch(error => {
          console.error(error);
        });
    },
    getEvents({ commit }, dateTimeRange, city) {
      // ! DEMO CODE ONLY
      let demoEvents = [
        {
          name: "Soccer match PSV - FC Utrecht",
          dateTime: "",
          location: {
            lat: "51.4417",
            long: "5.4674"
          },
          type: "sports"
        },
        {
          name: "Evoluon Techbeurs",
          dateTime: "",
          location: {
            lat: "51.4435",
            long: "5.4469"
          },
          type: "events"
        }
      ];
      commit("SET_EVENTS", demoEvents);

      // TODO Set up endpoint on backend

      // let searchQuery =
      //   "?from=" +
      //   dataTimeRange.from +
      //   "&to=" +
      //   dateTimeRange.to +
      //   "&city=" +
      //   city;

      // axios
      //   .get("/api/events/" + searchQuery)
      //   .then(result => {
      //     commit("SET_EVENTS", result.data);
      //   })
      //   .catch(error => {
      //     console.error(error);
      //   });
    }
  },
  getters: {
    getCalls: state => state.calls,
    getEvents: state => state.events,
    getCbs: state => state.neighborhoodData,
    getCbsKey: state => state.cbsDataKey
  }
});

function coordToGeoJson(coords, id) {
  //   // console.log(coords);
  //   coords.forEach(coord => {
  //     coord.latlng = L.latlng(coord.lat, coord.lon);
  //   });
  //   console.log(coords)
  return coords;
}
