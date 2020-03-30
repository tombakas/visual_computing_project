import Vue from 'vue';
import VueRouter from 'vue-router';
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue';

import App from './App.vue';
import store from './store';

// Views
import MapView from './components/MapView';
import Graphs from './components/Graphs';

Vue.use(BootstrapVue);

Vue.config.productionTip = false;
Vue.config.devtools = true;

Vue.use(VueRouter);

const router = new VueRouter({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Map',
      component: MapView,
      props: false
    },
    {
      path: '/graphs',
      name: 'Graphs',
      component: Graphs,
      props: false
    }
  ]
});

new Vue({
  store,
  router,
  render: h => h(App)
}).$mount('#app')
