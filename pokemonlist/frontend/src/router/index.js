import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/user'

// Importe seus componentes de view
import HomeView from '@/views/HomeView.vue'
import TeamsView from '@/views/TeamsView.vue'
import NotFoundView from '@/views/NotFoundView.vue' // Para rotas não encontradas
import PokemonSearch from '@/views/PokemonSearch.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/teams',
    name: 'teams',
    component: TeamsView,
    meta: {
      title: 'PokeList - Meus Times',
      requiresAuth: true // Rota protegida
    }
  },
  {
    path: '/search',
    name: 'search',
    component: PokemonSearch,
    meta: {
      title: 'PokeList - Pesquisa Pokémon'
    }
  },
  {
      path: '/pokemon/:name',
      name: 'Pokemon',
      component: () => import('@/views/Pokemon.vue'),
      meta: { requiresAuth: true },
      props: true
  },
  {
    path: '/:pathMatch(.*)*', // Captura todas as rotas não definidas
    name: 'not-found',
    component: NotFoundView,
    meta: {
      title: 'Página não encontrada'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guarda de navegação global
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  // Verifica autenticação antes de cada navegação
  await authStore.checkAuth()
  
  // Atualiza o título da página
  document.title = to.meta.title || 'PokeList'
  
  // Verifica se a rota requer autenticação
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!authStore.isLoggedIn) {
      // Redireciona para login se não estiver autenticado
      next({ name: 'home', query: { redirect: to.fullPath } })
      return
    }
  }
  
  // Verifica se a rota é apenas para visitantes (não logados)
  if (to.matched.some(record => record.meta.requiresGuest)) {
    if (authStore.isLoggedIn) {
      // Redireciona para home se já estiver logado
      next({ name: 'home' })
      return
    }
  }
  
  next()
})

export default router