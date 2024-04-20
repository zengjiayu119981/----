import { createApp } from 'vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import $ from 'jquery'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import 'bootstrap/dist/js/bootstrap.min.js'
import './assets/css/main.css'
import './assets/css/libs.min.css'
import './assets/js/libs.js'
import './assets/js/main.js'
import 'bootstrap-icons/font/bootstrap-icons.min.css'

import VueCookies from 'vue-cookies'

import router from './router/index.js'

import App from './App.vue'

import axios from './utils/require.js'

const app = createApp(App)
app.config.globalProperties.$axios=axios
app.config.globalProperties.$cookies=VueCookies
app.use(router)
app.mount('#app')