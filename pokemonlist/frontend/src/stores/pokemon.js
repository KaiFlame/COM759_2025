import { defineStore } from 'pinia'
import axios from 'axios'
import PokemonCard from '@/components/PokemonCard.vue' // ou ajuste o caminho se estiver em outro lugar


export const usePokemonStore = defineStore('pokemon', {
  state: () => ({
    pokemon: null,
    teams: []
  }),
  actions: {
    async fetchPokemon(name) {
      try {
        const response = await axios.get(`http://localhost:5000/pokemon/${name}`)
        this.pokemon = response.data
      } catch (err) {
        console.error('Erro ao buscar Pokémon:', err)
        this.pokemon = null
      }
    },

    async saveTeam(teamData) {
      try {
        await axios.post('http://localhost:5000/team', teamData, { withCredentials: true })
        console.log('Time salvo com sucesso:', teamData)
      } catch (err) {
        console.error('Erro ao salvar time:', err)
      }
    }
  }
})
