<template>
  <div class="not-found-container">
    <div class="not-found-content">
      <h1>404 - Página Não Encontrada</h1>
      <p>Oops! Parece que este Pokémon fugiu do laboratório!</p>
      
      <div class="pokemon-error">
        <img src="https://media.tenor.com/UZJd1pjj4NMAAAAe/surprised-pikachu.png" alt="Pikachu confuso" class="error-image">
        <p class="error-message">Pikachu está tão confuso quanto você!</p>
      </div>
      
      <router-link to="/" class="home-link">
        <span class="material-symbols-outlined">home</span>
        Voltar para o Laboratório Pokémon
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { useHead } from '@vueuse/head'

useHead({
  title: '404 - Página Não Encontrada | PokéList',
  meta: [
    {
      name: 'description',
      content: 'Página não encontrada - PokéList'
    }
  ]
})
</script>

<style scoped>
.not-found-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f5f5 0%, #e3f2fd 100%);
  padding: 2rem;
}

.not-found-content {
  text-align: center;
  max-width: 600px;
  padding: 2rem;
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  border: 2px solid #ffcb05; /* Amarelo Pokémon */
}

h1 {
  color: #2a75bb; /* Azul Pokémon */
  margin-bottom: 1rem;
}

p {
  color: #333;
  font-size: 1.1rem;
  margin-bottom: 2rem;
}

.pokemon-error {
  margin: 2rem 0;
}

.error-image {
  max-width: 200px;
  height: auto;
  margin-bottom: 1rem;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1));
}

.error-message {
  font-style: italic;
  color: #666;
}

.home-link {
  display: inline-flex;
  align-items: center;
  padding: 0.8rem 1.5rem;
  background-color: #2a75bb;
  color: white;
  text-decoration: none;
  border-radius: 50px;
  font-weight: bold;
  transition: all 0.3s ease;
  margin-top: 1rem;
    &:hover {
    background-color: #3b5ba7;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(43, 117, 187, 0.3);
  }

}



.home-link .material-symbols-outlined {
  margin-right: 0.5rem;
  font-size: 1.2rem;
}

@media (max-width: 600px) {
  .not-found-container {
    padding: 1rem;
  }
  
  .not-found-content {
    padding: 1.5rem;
  }
  
  h1 {
    font-size: 1.5rem;
  }
}
</style>