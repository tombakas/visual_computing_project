import Vue from 'vue';
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

import App from './App.vue';
import store from './store';

Vue.use(BootstrapVue)

Vue.config.productionTip = false;
Vue.config.devtools = true

new Vue({
  store,
  render: h => h(App)
}).$mount('#app')
