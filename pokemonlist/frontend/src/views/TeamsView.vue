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
      <a href="">
       {{ authStore.isLoggedIn ? authStore.username: '' }}</a>
      <button 
        class="loginBtn" 
        @click.prevent="authStore.isLoggedIn ? handleLogout() : redirectToHome()">
        {{ authStore.isLoggedIn ? 'Logout' : 'Login' }}
      </button>
    </nav>
  </header>

  <div class="team-container">
    <h1>Meu Time Pokémon</h1>
    
    <div v-if="!authStore.isLoggedIn" class="login-message">
      <p>Você precisa estar logado para acessar esta funcionalidade.</p>
      <button @click="redirectToHome" class="login-btn">Fazer Login</button>
    </div>

    <div v-else>
      <div v-if="teamStore.loading" class="loading">Carregando...</div>
      <div v-else>
        <div v-if="teamStore.error" class="error">{{ teamStore.error }}</div>
        
        <div v-if="teamStore.team.length === 0" class="empty-team">
          <p>Seu time está vazio. Adicione Pokémons na página de pesquisa!</p>
        </div>
        
        <div class="team-grid">
          <div v-for="pokemon in teamStore.team" :key="pokemon.id" class="team-member">
            <img :src="pokemon.sprites.front_default" :alt="pokemon.name" class="pokemon-sprite">
            <h3>{{ pokemon.name }}</h3>
            <button @click="removeFromTeam(pokemon.id)" class="remove-btn">
              <span class="material-symbols-outlined">delete</span>
            </button>
          </div>
        </div>
        
        <div class="team-info">
          <p>Pokémons no time: {{ teamStore.team.length }}/6</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/user'
import { useTeamStore } from '@/stores/team'

const router = useRouter()
const authStore = useAuthStore()
const teamStore = useTeamStore()

onMounted(() => {
  if (authStore.isLoggedIn) {
    teamStore.fetchTeam()
  }
})

const removeFromTeam = (pokemonId) => {
  if (confirm('Tem certeza que deseja remover este Pokémon do seu time?')) {
    teamStore.removePokemon(pokemonId)
  }
}


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
.team-container {
    display: flex;
    flex-direction: column;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
  font-family: "Quicksand", sans-serif;

    h1{
            background: transparent ;
            font-size: 22.5pt;
            font-family: "Quicksand", sans-serif;
            color: white;
            min-width: 25vw;    
            border-radius: 20px;
            backdrop-filter: blur(15px);
            padding: 10pt;
            text-shadow: 1px 1px 2px black;
        
    }

    p{
        background: transparent;
            border: 2px solid rgba($color: #ffffff98, $alpha: 1.0);
            max-width: 200px;
            font-size: 10pt;
            outline: none;
            font-family: "Quicksand", sans-serif;
            color: white;
            border-radius: 20px;
            backdrop-filter: blur(15px);
    }

}

.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 20px;
  margin-top: 30px;
}

.team-member {
  background: #fff;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  position: relative;
  transition: transform 0.3s;
}

.team-member:hover {
  transform: translateY(-5px);
}

.pokemon-sprite {
  width: 80px;
  height: 80px;
}

.remove-btn {
  position: absolute;
  top: 5px;
  right: 5px;
  background: #ff4444;
   color: white;
  border: none;
  border-radius:  50%;
  width: 25px;
  height: 25px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.remove-btn:hover 
{
  background: #cc0000;
}

.team-info {
   margin-top: 20px;
  font-size: 1.1em;
}

.empty-team, .login-message {
  margin-top: 50px;
  font-size: 1.2em;
}

.login-btn {
  margin-top: 15px;
  padding: 10px 20px;
   background: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.login-btn:hover {
  background: #45a049;
}

.loading, .error {
  margin-top: 20px;
  padding: 15px;
  border-radius: 5px;
}

.loading {
  background: #f0f0f0;
}

.error {
  background: #ffdddd;
  color: #ff0000;
}
</style>