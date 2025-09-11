// src/router/index.ts
import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('../pages/DashboardPage.vue'),
    meta: { title: 'Home' },
  },
  {
    path: '/pokemon/:name',
    name: 'pokemon-by-name',
    component: () => import('../pages/PokemonDetailsPage.vue'),
    props: (route) => ({ name: String(route.params.name) }),
    meta: { title: 'Pokémon' },
  },
  // 404 na końcu
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('../pages/NotFoundPage.vue'),
    meta: { title: '404' },
  },
]

const router = createRouter({
  history: createWebHistory(), // czyste URL-e (bez #)
  routes,
  scrollBehavior(_to, _from, saved) {
    return saved ?? { top: 0 }
  },
})

// Ustawianie <title> z meta
router.afterEach((to) => {
  document.title = (to.meta?.title as string) ?? 'My App'
})

export default router
