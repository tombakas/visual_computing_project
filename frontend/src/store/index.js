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
    events: []
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
    getCbs: state => state.neighborhoodData
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
