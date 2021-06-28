import 'core-js/stable'
import Vue from 'vue'
import CoreuiVuePro from '../node_modules/@coreui/vue-pro/src/index.js'
import App from './App'
import router from './router'
import {iconsSet as icons} from './assets/icons/icons.js'
import store from './store'
import i18n from './i18n.js'
import axiosApi from 'axios';
import 'vue-select/dist/vue-select.css';
import vSelect from "vue-select";
import VueLodash from 'vue-lodash'
import lodash from 'lodash'


let baseURL = process.env.VUE_APP_BASEURL;
let axios = null;

axios = axiosApi.create({
    baseURL: baseURL,
});

window.axios = axios;

Vue.use(CoreuiVuePro)
Vue.prototype.$log = console.log.bind(console)
Vue.component('v-select', vSelect)

new Vue({
    el: '#app',
    router,
    store,
    icons,
    i18n,
    template: '<App/>',
    components: {
        App
    }
})
