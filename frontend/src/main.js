import Vue from 'vue'
import VueRouter from 'vue-router'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import {VueMasonryPlugin} from 'vue-masonry'
import VueClipboard from 'vue-clipboard2'

import App from './App'
import router from './router'

Vue.config.productionTip = false

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
Vue.use(VueMasonryPlugin)
Vue.use(VueClipboard)
Vue.use(VueRouter)

// Global variables available to all components
const globalStore = new Vue({
  data: {
    slashCommand: '/hcc',
    backend: '',
    flockEventToken: null,
    flockTheme: null,
    flockEvent: null,
    imageMeta: null
  }
})
Vue.prototype.$globals = globalStore;

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')

// Bootstrap CSS styles
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'