import { createApp } from 'vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import $ from 'jquery'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import 'bootstrap/dist/js/bootstrap.min.js'
import '/src/assets/css/main.css'
import '/src/assets/css/libs.min.css'
import '/src/assets/js/libs.js'
import '/src/assets/js/main.js'
import 'bootstrap-icons/font/bootstrap-icons.min.css'

import axios from '../src/utils/require.js'

import router from '/src/router/index.js'

import login from './login.vue'

import VueCookies from 'vue-cookies'

const app = createApp(login)
app.config.globalProperties.$axios=axios
app.config.globalProperties.$cookies=VueCookies
app.use(router)
app.mount('#app')