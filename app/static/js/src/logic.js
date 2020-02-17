Vue.component("base-map", {
  data() {
    return {
      map: null
    };
  },
  mounted() {
    mapboxgl.accessToken = 'pk.eyJ1IjoiY2h1cnJvcyIsImEiOiJjazZxdHlkNWQwMGViM21wZHMzMWRxazBvIn0.tdWPYNbC-n38mpRA23WFyQ';
    let map = new mapboxgl.Map({
      container: 'map',
      style: 'mapbox://styles/mapbox/streets-v11',
      center: [5.4697, 51.4416],
      zoom: 11.5,
    });
  },
  template: "<div id='map' style='width: 100%; height: 100%;'></div>"
});

Vue.component('navigation-bar', {
  template: "<nav><h1>App name</h1></nav>"
})

var app = new Vue({
  el: "#app",
  data: {
    message: "Most awesomest visualazation project like ever!"
  }
});
