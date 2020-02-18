import Vue from 'vue';
import VueRouter from 'vue-router';
Vue.use(VueRouter);

import China  from './components/China.vue';
import Map  from './components/Map.vue';
// import user   from './components/China.vue'

const routes = [
    {
        path: '', 
        component: China
    },
    {
        path: '/china', 
        component: China
    },
    {
        path: '/province', 
        component: China
    },
    {
        path: '/map', 
        component: Map
    },
]

const router = new VueRouter({
    routes
});

export default router

