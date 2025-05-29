import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isAuthenticated: false
  }),

  getters: {
    isLoggedIn: (state) => state.isAuthenticated,
    username: (state) => state.user?.username || 'Usuário'
  },

  actions: {
    async login(userData) {
    try {
      // Limpa qualquer estado residual antes do novo login
      this.user = null
      this.isAuthenticated = false
      
      // Atualiza com os novos dados
      this.user = userData
      this.isAuthenticated = true
      localStorage.setItem('user', JSON.stringify(userData))
    } catch (error) {
      console.error('Erro ao fazer login:', error)
      throw error
    }
  },

  async logout() {
    try {
      // Limpa completamente o estado
      this.user = null
      this.isAuthenticated = false
      localStorage.removeItem('user')
      
      // Adiciona um passo extra para garantir a limpeza
      localStorage.clear() // Limpa todo o localStorage (opcional)
    } catch (error) {
      console.error('Erro ao fazer logout:', error)
      throw error
    }
  },

    async checkAuth() {
      try {
        const storedUser = localStorage.getItem('user')
        if (storedUser) {
          this.user = JSON.parse(storedUser)
          this.isAuthenticated = true
          return true
        }
        return false
      } catch (error) {
        console.error('Erro ao verificar autenticação:', error)
        return false
      }
    }
  }
})