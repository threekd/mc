import { createRouter, createWebHistory } from 'vue-router';
import AppLayout from '@/layout/AppLayout.vue';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: AppLayout,
            children: [
                {
                    path: '/',
                    name: 'Start',
                    component: () => import('@/views/Start.vue')
                },
                {
                    path: '/cfmid',
                    name: 'cfmid',
                    component: () => import('@/views/pages/CFMID.vue')
                },
                {
                    path: '/predictivemodel',
                    name: 'predictivemodel',
                    component: () => import('@/views/pages/predictivemodel.vue')
                },
                {
                    path: '/machinelearning',
                    name: 'machinelearning',
                    component: () => import('@/views/pages/machinelearning.vue')
                }
            ]
        }
    ]
});

export default router;
