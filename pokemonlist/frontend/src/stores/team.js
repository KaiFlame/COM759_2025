import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useTeamStore = defineStore('team', () => {

  const team = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchTeam = async () => {
    try {
      loading.value = true
      const response = await fetch('http://localhost:5000/team', {
        credentials: 'include'
      })

      const data = await response.json()
      team.value = data.pokemons || []
    } catch (err) {
      error.value = err.message
    } 
    
    finally {
      loading.value = false
    }
  }

// add
  const addPokemon = async (pokemon) => {
    try {
      loading.value = true
      const response = await fetch('http://localhost:5000/team', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ pokemon }),
        credentials: 'include'
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Falha ao adicionar Pokémon')
      }
      
      await fetchTeam() // Atualiza o time após adição
      return true
    } catch (err) {
      error.value = err.message
      return false
    } finally 
    {
      loading.value = false
    }
  }

  const removePokemon = async (pokemonId) => {
    try {
      loading.value = true
      const response = await fetch(`http://localhost:5000/team?pokemon_id=${pokemonId}`, {
        method: 'DELETE',
        credentials: 'include'
      })
      

      if (!response.ok) {
        throw new Error('Falha ao remover Pokémon')
      }
      
      await fetchTeam() // Atualiza o time após remoção
    } catch (err) {
      error.value = err.message
    } 
    finally {
      loading.value = false


    }
  }

  return { team, loading, error, fetchTeam, addPokemon, removePokemon }
})