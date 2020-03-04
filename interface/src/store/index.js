import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    calls: [],
    timePeriod: {
      from: '',
      to: ''
    },
    dispatchType: {},
    neighborhood: {}
  },
  mutations: {
    SET_DATA(state, calls) {
      state.calls = calls;
    },
    SET_TIME_PERIOD(state, timePeriod) {
      state.timePeriod = timePeriod;
    }
  },
  actions: {
    setTimePeriod({ commit }, timePeriod) {
      commit("SET_TIME_PERIOD", timePeriod);
    },
    getLatest({ commit }) {
      let demoGeoJson = {
        type: 'geojson',
        data: {
          id: "thisIsMySource",
          type: "FeatureCollection",
          features: [
          {
            "type": "Feature",
            "properties": {
            },
            "geometry": {
              "type": "Point",
              "coordinates": [
                5.472650527954102,
                51.44352269273299
              ]
            }
          },
          {
            "type": "Feature",
            "properties": {},
            "geometry": {
              "type": "Point",
              "coordinates": [
                5.482349395751953,
                51.43811917142602
              ]
            }
          },
          {
            "type": "Feature",
            "properties": {},
            "geometry": {
              "type": "Point",
              "coordinates": [
                5.497884750366211,
                51.43865420205084
              ]
            }
          },
          {
            "type": "Feature",
            "properties": {},
            "geometry": {
              "type": "Point",
              "coordinates": [
                5.486040115356445,
                51.429825395309614
              ]
            }
          },
          {
            "type": "Feature",
            "properties": {},
            "geometry": {
              "type": "Point",
              "coordinates": [
                5.453939437866211,
                51.43897521741748
              ]
            }
          },
          {
            "type": "Feature",
            "properties": {},
            "geometry": {
              "type": "Point",
              "coordinates": [
                5.461492538452148,
                51.42072726427204
              ]
            }
          },
          {
            "type": "Feature",
            "properties": {},
            "geometry": {
              "type": "Point",
              "coordinates": [
                5.472650527954102,
                51.44352269273299
              ]
            }
          },
          {
            "type": "Feature",
            "properties": {},
            "geometry": {
              "type": "Point",
              "coordinates": [
                5.482349395751953,
                51.43811917142602
              ]
            }
          },
          {
            "type": "Feature",
            "properties": {},
            "geometry": {
              "type": "Point",
              "coordinates": [
                5.497884750366211,
                51.43865420205084
              ]
            }
          },
          {
            "type": "Feature",
            "properties": {},
            "geometry": {
              "type": "Point",
              "coordinates": [
                5.486040115356445,
                51.429825395309614
              ]
            }
          },
          {
            "type": "Feature",
            "properties": {},
            "geometry": {
              "type": "Point",
              "coordinates": [
                5.453939437866211,
                51.43897521741748
              ]
            }
          },
          {
            "type": "Feature",
            "properties": {},
            "geometry": {
              "type": "Point",
              "coordinates": [
                5.461492538452148,
                51.42072726427204
              ]
            }
          }
        ]
        }
      };

    
      commit("SET_DATA", demoGeoJson);
      // axios.get('api/calls/latest').then(result => {
      //   commit("SET_DATA", result); // TODO: verify json response structure
      // }).catch(error => {
      //   console.error(error);
      // });
    },
    getCalls({ commit }, params) {
      let requestParams = '?';
      for (let param in params) {
        requestParams += `${param}: ${params[param]}`;
      }
      axios.get('api/calls' + requestParams).then(result => {
        commit("SET_DATA", result); // TODO: verify json response structure
      }).catch(error => {
        console.error(error);
      });
    }
  },
  getters: {
    getCalls: state => state.calls,
  },
})
