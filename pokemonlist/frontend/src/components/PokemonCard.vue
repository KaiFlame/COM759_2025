<template>
  <div class="pokemon-card">
    <img :src="pokemon.sprites.front_default" :alt="pokemon.name">
    <h3>{{ capitalize(pokemon.name) }}</h3>
    <div class="buttons-container">
      <button class="details-btn" @click="viewDetails">Ver Detalhes</button>
      <button class="add-btn add-to-team-btn" @click="addToTeam" v-if="authStore.isLoggedIn" :disabled="isInTeam">Adicionar ao time</button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/user'
import { useTeamStore } from '@/stores/team'
import { usePokemonStore } from '@/stores/pokemon'
import { defineProps } from 'vue'
import { useRouter } from 'vue-router'

const pokemonStore = usePokemonStore()
const router = useRouter()


const props = defineProps({
  pokemon: Object
})

const authStore = useAuthStore()
const teamStore = useTeamStore()

const isInTeam = computed(() => {
  return teamStore.team.some(p => p.id === props.pokemon.id)
})

const addToTeam = async () => {
  if (isInTeam.value) return
  
  const pokemonData = {
    id: props.pokemon.id,
    name: props.pokemon.name,
    sprites: {
      front_default: props.pokemon.sprites.front_default
    }
    // Adicione outros dados que você quer salvar
  }
  
  const success = await teamStore.addPokemon(pokemonData)
  if (success) {
    alert('Pokémon adicionado ao time com sucesso!')
  }
}

// Página de detalhes do Pokémon selecionado
const viewDetails = () => {
  router.push(`/pokemon/${props.pokemon.id}`)
}

const capitalize = (str) => str.charAt(0).toUpperCase() + str.slice(1)



</script>

<style lang="scss" scoped>

.s-pok input{
  background: transparent;
}


.pokemon-card {
  margin-top: 20px;
  background: white;
  border-radius: 8px;
  padding: 1rem;
  margin: 1rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-align: center;
  font-family: "WDXL Lubrifont TC", sans-serif;
  transition: transform 0.2s ease;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
  }

  img {
    width: 120px;
    height: auto;
  }

  h3 {
    margin: 0.5rem 0;
    color: #333;
  }

  .buttons-container {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-top: 1rem;
  }

  button {
    border: none;
    border-radius: 5px;
    padding: 0.5rem 1rem;
    cursor: pointer;
    font-family: "WDXL Lubrifont TC", sans-serif;
    transition: background-color 0.2s ease;
    width: 100%;

    &.details-btn {
      background-color: #3498db;
      color: white;

      &:hover {
        background-color: #2980b9;
      }
    }

    &.add-btn {
      background-color: #f1c40f;
      color: #333;

      &:hover {
        background-color: #d4ac0d;
      }
    }
  }
}
</style>