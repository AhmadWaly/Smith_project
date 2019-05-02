import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import BootstrapVue from "bootstrap-vue";
import VueResource from 'vue-resource';
import Vuelidate from 'vuelidate'
import VueSweetalert2 from 'vue-sweetalert2';
import Loading from 'vue-loading-overlay';

import 'vue-loading-overlay/dist/vue-loading.css';
import 'tracking/build/tracking-min'
import 'tracking/build/data/face-min'
import 'vue-cam'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(Loading);
Vue.use(BootstrapVue);
Vue.use(VueResource);
Vue.use(Vuelidate);
Vue.use(VueSweetalert2);
Vue.config.productionTip = false;

new Vue({
  router,
  render: h => h(App)
}).$mount("#app");
