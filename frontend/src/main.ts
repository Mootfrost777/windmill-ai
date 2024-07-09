import { createApp } from 'vue'
import { createMemoryHistory, createRouter } from 'vue-router'
import Notifications from '@kyvg/vue3-notification'



import './style.css'
import App from './App.vue'
import Dashboard from "./components/Dashboard.vue";

const routes = [
    { path: '/', component: Dashboard }
]

const router = createRouter({
    history: createMemoryHistory(),
    routes,
})

createApp(App)
    .use(router)
    .use(Notifications)
    .mount('#app')
