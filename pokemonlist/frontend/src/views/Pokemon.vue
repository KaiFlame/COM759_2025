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
        {{ authStore.isLoggedIn ? authStore.username : '' }}
      </a>
      <button 
        class="loginBtn" 
        @click.prevent="authStore.isLoggedIn ? handleLogout() : redirectToHome()">
        {{ authStore.isLoggedIn ? 'Logout' : 'Login' }}
      </button>
    </nav>
  </header>

   <div class="pokemon-details-container" v-if="pokemon">
    <div class="pokemon-header">
      <button class="back-button" @click="goBack">← Voltar</button>
      <h1>{{ capitalize(pokemon.name) }} <span class="pokemon-id">#{{ String(pokemon.id).padStart(3, '0') }}</span></h1>
    </div>

    <div class="pokemon-main-content">
      <!-- Seção Esquerda - Imagem e Tipos -->
      <div class="pokemon-image-section">
        <img :src="pokemon.sprites.other['official-artwork'].front_default || pokemon.sprites.front_default" 
             :alt="pokemon.name"
             class="pokemon-image">
        
        <div class="types-container">
          <span v-for="t in pokemon.types" 
                :key="t.type.name"
                class="pokemon-type"
                :class="'type-' + t.type.name">
            {{ capitalize(t.type.name) }}
          </span>
        </div>
      </div>

      <!-- Seção Direita - Detalhes -->
      <div class="pokemon-info-section">
        <!-- Informações Básicas -->
        <div class="info-card">
          <h2>📊 Informações Básicas</h2>
          <div class="info-grid">
            <div><strong>Altura:</strong> {{ (pokemon.height / 10).toFixed(1) }} m</div>
            <div><strong>Peso:</strong> {{ (pokemon.weight / 10).toFixed(1) }} kg</div>
            <div><strong>Experiência:</strong> {{ pokemon.base_experience }} XP</div>
            <div><strong>Ordem:</strong> #{{ pokemon.order }}</div>
          </div>
        </div>

        <!-- Stats -->
        <div class="info-card">
          <h2>⚔️ Estatísticas</h2>
          <div class="stats-container">
            <div v-for="stat in pokemon.stats" :key="stat.stat.name" class="stat-item">
              <div class="stat-name">{{ capitalize(stat.stat.name.replace('-', ' ')) }}</div>
              <div class="stat-bar-container">
                <div class="stat-bar" :style="{ width: (stat.base_stat / 255 * 100) + '%' }"></div>
              </div>
              <div class="stat-value">{{ stat.base_stat }}</div>
            </div>
          </div>
        </div>

        <!-- Habilidades -->
        <div class="info-card">
          <h2>✨ Habilidades</h2>
          <div class="abilities-container">
            <div v-for="a in pokemon.abilities" :key="a.ability.name" class="ability">
              {{ capitalize(a.ability.name.replace('-', ' ')) }}
              <span v-if="a.is_hidden" class="hidden-ability">(habilidade oculta)</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Movimentos -->
    <div class="pokemon-moves-section">
      <h2>🎯 Movimentos</h2>
      <div class="moves-container">
        <div v-for="move in filteredMoves" :key="move.move.name" class="move-card">
          <h3>{{ capitalize(move.move.name.replace('-', ' ')) }}</h3>
          <div v-for="v in move.version_group_details" :key="v.version_group.name" class="move-detail">
            <span class="learn-method">{{ capitalize(v.move_learn_method.name.replace('-', ' ')) }}</span>
            <span v-if="v.level_learned_at > 0"> no nível {{ v.level_learned_at }}</span>
            <span class="game-version">({{ v.version_group.name }})</span>
          </div>
        </div>
      </div>
      <button v-if="showAllMoves" @click="showAllMoves = false" class="show-less">Mostrar menos</button>
      <button v-else @click="showAllMoves = true" class="show-more">Mostrar mais (+{{ pokemon.moves.length - 8 }} movimentos)</button>
    </div>
  </div>


  <div v-else class="loading-container">
    <div class="loading-spinner"></div>
    <p>Carregando informações do Pokémon...</p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue' 
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/user'


const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const pokemon = ref(null)

// Autenticação ao carregar
onMounted(async () => {
  // Se o usuário está autenticado
  if (!authStore.isLoggedIn) {
    router.push('/login')
    return
  }

  try {
    const response = await fetch(`http://127.0.0.1:5000/pokemon/${route.params.name}`)
    if (!response.ok) throw new Error('Pokémon não encontrado')
    pokemon.value = await response.json()
  } catch (error) {
    console.error('Erro ao carregar Pokémon:', error)
    router.push('/not-found')
  }
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

const showAllMoves = ref(false)
const movesToShowInitially = 8

// Computed property filtrar os movimentos
const filteredMoves = computed(() => {
  if (!pokemon.value) return []
  return showAllMoves.value 
    ? pokemon.value.moves 
    : pokemon.value.moves.slice(0, movesToShowInitially)
})

const redirectToHome = () => {
  router.push('/login')
}

const goBack = () => {
  router.go(-1)
}

const capitalize = (str) => {
  if (!str) return ''
  return str.charAt(0).toUpperCase() + str.slice(1)
}
</script>

<style scoped lang="scss">
@import '@/assets/scss/home.scss';

.pokemon-details-container {
  max-width: 1200px;
  margin: 0 auto;
   margin-top: 100px;
  padding: 1rem;
  font-family: "WDXL Lubrifont TC", sans-serif;
   color: #333;
}

.pokemon-header {
  display: flex;
  align-items: center;
  margin-bottom: 2rem;
  position: relative;

  h1 {
    flex-grow: 1;
    text-align: center;
    font-size: 2.5rem;
    color: #2c3e50;
    margin: 0;
  }

  .pokemon-id {
    color: #7f8c8d;
    font-size: 1.5rem;
  }

  .back-button {
    background-color: #f1c40f;
    border: none;
    border-radius: 5px;
    padding: 0.5rem 1rem;
    cursor: pointer;
    font-family: "WDXL Lubrifont TC", sans-serif;
    transition: background-color 0.2s ease;

    &:hover {
      background-color: #d4ac0d;
    }
  }
}

.pokemon-main-content {
  display: flex;
  flex-wrap: wrap;
   gap: 2rem;
  margin-bottom: 2rem;

  @media (max-width: 768px) {
    flex-direction: column;
  }
}

.pokemon-image-section {
  flex: 1;
  min-width: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);

  .pokemon-image {
    width: 100%;
    max-width: 400px;
    height: auto;
    margin-bottom: 1.5rem;
  }
}

.types-container {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;

  .pokemon-type {
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
     color: white;
    font-weight: bold;
    text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    text-transform: capitalize;
  }

  /* Cores para cada tipo de pokemon*/
  .type-normal { background-color: #A8A878; }
  .type-fire { background-color: #F08030; }
  .type-water { background-color: #6890F0; }
  .type-electric { background-color: #F8D030; }
  .type-grass { background-color: #78C850; }
  .type-ice { background-color: #98D8D8; }
  .type-fighting { background-color: #C03028; }
  .type-poison { background-color: #A040A0; }
  .type-ground { background-color: #E0C068; }
  .type-flying { background-color: #A890F0; }
  .type-psychic { background-color: #F85888; }
  .type-bug { background-color: #A8B820; }
  .type-rock { background-color: #B8A038; }
  .type-ghost { background-color: #705898; }
  .type-dragon { background-color: #7038F8; }
  .type-dark { background-color: #705848; }
  .type-steel { background-color: #B8B8D0; }
  .type-fairy { background-color: #EE99AC; }
}

.pokemon-info-section {
   flex:  2;
  min-width: 300px;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.info-card {
  background: white;
  border-radius:  12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);

  h2 {
    margin-top: 0;
    margin-bottom: 1rem;
    color: #2c3e50;
    font-size: 1.5rem;
    border-bottom: 2px solid #f1c40f;
    padding-bottom: 0.5rem;
  }
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;



  div {
    padding: 0.5rem;
    background: #f8f9fa;
    border-radius: 5px;
  }
}

.stats-container {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 1rem;

  .stat-name {
    min-width: 120px;
    text-align: right;
  }

  .stat-bar-container {
    flex-grow: 1;
    height: 20px;
    background: #ecf0f1;
    border-radius: 10px;
    overflow: hidden;
  }
  .stat-bar {
    height: 100%;
    background: linear-gradient(90deg, #f1c40f, #e67e22);
    border-radius: 10px;
  }

  .stat-value {
    min-width: 30px;
    text-align: right;
    font-weight: bold;
  }
}

.abilities-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
.ability {
    background: #3498db;
    color: white;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-size: 0.9rem;
  }

  .hidden-ability {
    font-size: 0.8rem;
    opacity: 0.8;
  }
}

.pokemon-moves-section {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-top: 2rem;
h2 {
    margin-top: 0;
    color: #2c3e50;
    font-size: 1.5rem;
    border-bottom: 2px solid #f1c40f;
    padding-bottom: 0.5rem;
  }
}

.moves-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.move-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 1rem;
  transition: transform 0.2s;
  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    cursor: pointer;
  }

  h3 {
    margin-top: 0;
    color: #2c3e50;
    font-size: 1.1rem;
  }
}

.move-detail {
  font-size: 0.9rem;
  margin-top: 0.3rem;
  color: #7f8c8d;

  .learn-method {
    font-weight: bold;
    color: #3498db;
  }

  .game-version {
    font-style: italic;
  }
}

button.show-more, button.show-less {
  display: block;
  margin: 1.5rem auto 0;
  background-color: #3498db;
  color: white;
  border: none;
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.2s;

  &:hover {
    background-color: #2980b9;
  }
}
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 50vh;

  .loading-spinner {
    border: 5px solid #f3f3f3;
    border-top: 5px solid #f1c40f;
    border-radius: 50%;
    width: 50px;
    height: 50px;
    animation: spin 1s linear infinite;
    margin-bottom: 1rem;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
}
</style>
