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
      a_00_14: { key: 'Age 0-14', queried: false},
      a_15_24: { key: 'Age 15-24', queried: false},
      a_25_44: { key: 'Age 25-44', queried: false},
      a_45_64: { key: 'Age 45-64', queried: false},
      a_65_oo: { key: 'Age 65+', queried: false},
      a_ao: { key: 'Disability allowance', queried: false},
      a_aow: { key: 'Old age pension', queried: false},
      a_bijstand: { key: 'Social security payments', queried: false},
      a_car: { key: '#cars', queried: false},
      a_comp: { key: '#companies', queried: false},
      a_died: { key: '#died', queried: false},
      a_female: { key: '#females', queried: false},
      a_hh: { key: '#households', queried: false},
      a_house: { key: '#houses', queried: false},
      a_inc_rec: { key: '#income recipients', queried: false},
      a_inh: { key: '#inhabitants', queried: false},
      a_lan_ac: { key: 'Area in acres', queried: false},
      a_male: { key: '#males', queried: false},
      a_nw_all: { key: '#non-western persons', queried: false},
      a_sur_ac: { key: 'Surface area in acres', queried: false},
      a_w_all: { key: '#western persons', queried: false},
      a_wat_ac: { key: 'Water area in acres', queried: false},
      a_ww: { key: '#persons in unemployment security', queried: false},
      av_assault: {key: '#assaults (avg)', queried: false},
      av_car_hh: { key: '#cars per household (avg)', queried: false},
      av_des_po: { key: '#destruction and public misbehavior (avg)', queried: false},
      av_hh_size: { key: 'Average household size', queried: false},
      av_hou_theft: { key: '#theft in houses (avg)', queried: false},
      av_inc_inh_x1000: { key: 'Income per 1000 (avg)', queried: false},
      av_inc_rec_x1000: { key: 'Average income per income recipient x1000', queried: false},
      av_km_dc: { key: 'Distance to daycare in km (avg)', queried: false},
      av_km_doc: { key: 'Distance to gp in km (avg)', queried: false},
      av_km_sc: { key: 'Distance to school in km (avg)', queried: false},
      av_km_sup: { key: 'Distance to supermarket in km (avg)', queried: false},
      av_prop_val_x1000: { key: 'Property value x1000 (avg)', queried: false},
      city_name: { key: 'Name of city', queried: false},
      p_hh_usm: { key: 'Percentage of households under social minimum', queried: false},
      p_n_act: { key: 'Percentage of working people', queried: false},
      per_build_af_2000: { key: 'Percentage houses built after 2000', queried: false},
      per_build_be_2000: { key: 'Percentage houses built before 2000', queried: false},
      per_own_occ: { key: 'Percentage occupied houses', queried: false},
      per_ren_hou: { key: 'Percentage of rental houses', queried: false},
      per_uninhab: { key: 'Percentage of houses uninhabited', queried: false},
      pop_den_km2: { key: 'Population density per km2 ', queried: false},
      region: { key: 'Neighborhood name', queried: false}
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
