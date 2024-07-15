import { createApp } from 'vue'
import { createMemoryHistory, createRouter } from 'vue-router'
import Notifications from '@kyvg/vue3-notification'
import { createI18n } from 'vue-i18n'
import { VueQueryPlugin } from '@tanstack/vue-query'


import './style.css'
import App from './App.vue'
import Dashboard from "./components/Dashboard.vue";

import messages from '@intlify/unplugin-vue-i18n/messages'
import axios from "axios";

const routes = [
    { path: '/', component: Dashboard }
]

const router = createRouter({
    history: createMemoryHistory(),
    routes,
})

const i18n = createI18n({
    locale: 'ru',
    messages
})

axios.defaults.baseURL = import.meta.env.VITE_APP_API_ENDPOINT

createApp(App)
    .use(router)
    .use(Notifications)
    .use(i18n)
    .use(VueQueryPlugin)
    .mount('#app')
