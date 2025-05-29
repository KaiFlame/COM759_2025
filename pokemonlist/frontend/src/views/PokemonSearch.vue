<template>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&icon_names=maillockpersonsearch" />
  <link href="https://fonts.googleapis.com/css2?family=WDXL+Lubrifont+TC&display=swap" rel="stylesheet">

  <header>
    <h2>
      <img src="../assets/pokelist.png" alt="Pokelist Logo">
    </h2>
    <nav class="navigation">
      <a href="/teams" v-if="authStore.isLoggedIn">Meus Times</a>
      <a href="/search">Pesquisa Pokemon</a>
      <a href="/">
       {{ authStore.isLoggedIn ? ('Treinador ' + authStore.username): '' }}</a>
      <button 
        class="loginBtn" 
        @click.prevent="authStore.isLoggedIn ? handleLogout() : redirectToHome()">
        {{ authStore.isLoggedIn ? 'Logout' : 'Login' }}
      </button>
    </nav>
  </header>

  <div class="s-pok">
    <div class="bar">
      <input 
        v-model="pokemonName" 
        placeholder="Digite um Pokémon"
        @keyup.enter="fetchPokemon"
        @input="handleInput"
      >
      <button @click="fetchPokemon">
        <span class="material-symbols-outlined">search</span>
      </button>
      
      <!-- sugestões que podem ser feitas-->
      <div v-if="suggestions.length > 0" class="suggestions-dropdown">
        <div 
          v-for="pokemon in filteredSuggestions" 
          :key="pokemon.name"
          class="suggestion-item"
          @click="selectSuggestion(pokemon.name)"
        >
          {{ pokemon.name }}
        </div>
      </div>
    </div>

    <PokemonCard v-if="pokemonStore.pokemon" :pokemon="pokemonStore.pokemon" />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { usePokemonStore } from '@/stores/pokemon'
import { useAuthStore } from '@/stores/user'
import PokemonCard from '@/components/PokemonCard.vue'

const pokemonName = ref('')
const pokemonStore = usePokemonStore()
const router = useRouter()
const authStore = useAuthStore()
const suggestions = ref([])
const allPokemons = ref([])

onMounted(async () => {
  // Verifica se há dados de autenticação no carregamento
  const storedUser = localStorage.getItem('user')
  if (storedUser) {
    authStore.user = JSON.parse(storedUser)
    authStore.isAuthenticated = true
  }
  
  // Carrega a lista de todos os Pokémons para sugestões
  await loadAllPokemons()
})

const loadAllPokemons = async () => {
  try {
    const response = await fetch('https://pokeapi.co/api/v2/pokemon?limit=1000')
    const data = await response.json()
    allPokemons.value = data.results
  } catch (error) {
    console.error('Erro ao carregar lista de Pokémons:', error)
  }
}


const fetchPokemon = () => {
  if (pokemonName.value.trim()) {
    pokemonStore.fetchPokemon(pokemonName.value.toLowerCase())
    suggestions.value = [] // Limpa sugestões após pesquisa
  }
}

const handleInput = () => {
  if (pokemonName.value.length > 1) {
    // Filtra sugestões baseado no texto digitado
    suggestions.value = allPokemons.value.filter(pokemon => 
      pokemon.name.includes(pokemonName.value.toLowerCase()))
  } else {
    suggestions.value = []
  }
}

const selectSuggestion = (name) => {
  pokemonName.value = name
  fetchPokemon()
}

const filteredSuggestions = computed(() => {
  return suggestions.value.slice(0, 5) 
})


const handleLogout = async () => {
  try {
    await fetch('http://localhost:5000/logout', {
      method: 'POST',
      credentials: 'include'
    })
    authStore.logout()
    window.location.reload() 
  } catch (error) {
    console.error('Erro ao fazer logout:', error)
  }
}

const redirectToHome = () => {
  router.push('/')
}
</script>

<style lang="scss">
@import '@/assets/scss/home.scss';
@import '@/assets/scss/search.scss';

.suggestions-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(15px);
  border: 2px solid rgba(255, 255, 255, 0.6);
  border-radius: 0 0 20px 20px;
  border-top: none;
  z-index: 100;
  max-height: 200px;
  overflow-y: auto;
  margin-top: -2px;
}

.suggestion-item {
  padding: 15px 20px;
  color: white;
  font-family: "Quicksand", sans-serif;
  font-size: 18pt;
  cursor: pointer;
  transition: background-color 0.2s;
  
  &:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }
  
  &:not(:last-child) {
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  }
  
  &:last-child {
    border-radius: 0 0 18px 18px; 
  }
}

.bar {
  position: relative;
  
  input {
    &:focus {
      border-radius: 20px 20px 0 0 !important;
      border-bottom: 2px solid rgba(255, 255, 255, 0.6) !important;
    }
  }
}
</style>