import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    calls: [],
    timePeriod: {
      from: "",
      to: ""
    },
    dispatchType: {},
    neighborhood: {},
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
    }
  },
  actions: {
    setTimePeriod({ commit }, timePeriod) {
      commit("SET_TIME_PERIOD", timePeriod);
    },
    getLatest({ commit }) {
      let demoGeoJson = {
        type: "geojson",
        data: {
          id: "thisIsMySource",
          type: "FeatureCollection",
          features: [
            {
              type: "Feature",
              properties: {},
              geometry: {
                type: "Point",
                coordinates: [5.472650527954102, 51.44352269273299]
              }
            },
            {
              type: "Feature",
              properties: {},
              geometry: {
                type: "Point",
                coordinates: [5.482349395751953, 51.43811917142602]
              }
            },
            {
              type: "Feature",
              properties: {},
              geometry: {
                type: "Point",
                coordinates: [5.497884750366211, 51.43865420205084]
              }
            },
            {
              type: "Feature",
              properties: {},
              geometry: {
                type: "Point",
                coordinates: [5.486040115356445, 51.429825395309614]
              }
            },
            {
              type: "Feature",
              properties: {},
              geometry: {
                type: "Point",
                coordinates: [5.453939437866211, 51.43897521741748]
              }
            },
            {
              type: "Feature",
              properties: {},
              geometry: {
                type: "Point",
                coordinates: [5.461492538452148, 51.42072726427204]
              }
            },
            {
              type: "Feature",
              properties: {},
              geometry: {
                type: "Point",
                coordinates: [5.472650527954102, 51.44352269273299]
              }
            },
            {
              type: "Feature",
              properties: {},
              geometry: {
                type: "Point",
                coordinates: [5.482349395751953, 51.43811917142602]
              }
            },
            {
              type: "Feature",
              properties: {},
              geometry: {
                type: "Point",
                coordinates: [5.497884750366211, 51.43865420205084]
              }
            },
            {
              type: "Feature",
              properties: {},
              geometry: {
                type: "Point",
                coordinates: [5.486040115356445, 51.429825395309614]
              }
            },
            {
              type: "Feature",
              properties: {},
              geometry: {
                type: "Point",
                coordinates: [5.453939437866211, 51.43897521741748]
              }
            },
            {
              type: "Feature",
              properties: {},
              geometry: {
                type: "Point",
                coordinates: [5.461492538452148, 51.42072726427204]
              }
            }
          ]
        }
      };
      // commit("SET_DATA", demoGeoJson);
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
        requestParams += `${param}: ${params[param]}`;
      }
      axios
        .get("http://localhost:5000/api/calls" + requestParams)
        .then(result => {
          commit("SET_DATA", coordToGeoJson(result.data));
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
    getEvents: state => state.events
  }
});

function coordToGeoJson(coords, id) {
  let geoJson = {
    type: "geojson",
    data: {
      id: id,
      type: "FeatureCollection",
      features: []
    }
  };

  coords.forEach(coord => {
    let geoObject = {
      type: "Feature",
      properties: {
        dateTime: coord.datetime,
        urgency: coord.urgency,
        service: coord.service
      },
      geometry: {
        type: "Point",
        coordinates: [coord.lon, coord.lat]
      }
    };
    geoJson.data.features.push(geoObject);
  });
  return geoJson;
}
