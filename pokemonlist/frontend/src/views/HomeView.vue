<template>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&icon_names=maillockperson" />
  <link href="https://fonts.googleapis.com/css2?family=WDXL+Lubrifont+TC&display=swap" rel="stylesheet">
    
  <header>
    <h2>
      <img src="../assets/pokelist.png" alt="">
    </h2>
    <nav class="navigation">
      <a href="/teams" v-if="authStore.isLoggedIn">Meus Times</a>
      <a href="/search">Pesquisa Pokemon</a>
      <button 
        class="loginBtn" 
        @click.prevent="authStore.isLoggedIn ? handleLogout() : toggleLogin(true)">
        {{ authStore.isLoggedIn ? 'Logout' : 'Login' }}
      </button>
    </nav>
  </header> 

  <div class="wrapper" :class="{ 'active': isWrapperActive, 'active-popup': isLogging }">
    <span class="icon-close" @click.prevent="toggleLogin(false)">
      <span class="material-symbols-outlined">
        close
      </span>
    </span>

    <!-- Formulário de Login -->
    <div class="form-box login">
      <h2>Login</h2>
      <form @submit.prevent="handleLogin">                                               
        <div class="input-box">
          <span class="icon"><span class="material-symbols-outlined">mail</span></span>
          <input type="text" v-model="loginForm.username" required>
          <label>Usuário</label>
        </div>
        <div class="input-box">
          <span class="icon"><span class="material-symbols-outlined">lock</span></span>
          <input type="password" v-model="loginForm.password" required>
          <label>Senha</label>
        </div>
        <div class="remember-forgot">
          <label><input type="checkbox">Lembre de mim!</label>
          <a href="#">Esqueceu a senha?</a>
        </div>
        <button type="submit" class="btn">Login</button>
        <div class="login-register">
          <p>Não tem uma conta?<a href="" class="cadastro-link" @click.prevent="toggleWrapper(true)">Crie uma!</a></p>
        </div>
        <p v-if="loginError" class="error-message">{{ loginError }}</p>
      </form>
    </div>

    <!-- Formulário de Cadastro -->
    <div class="form-box cadastro">
      <h2>Criar Conta</h2>
      <form @submit.prevent="handleRegister">      
        <div class="input-box">
          <span class="icon"><span class="material-symbols-outlined">person</span></span>
          <input type="text" v-model="registerForm.username" required>
          <label>Usuário</label>
        </div>                                         
        <div class="input-box">
          <span class="icon"><span class="material-symbols-outlined">mail</span></span>
          <input type="email" v-model="registerForm.email" required>
          <label>Email</label>
        </div>
        <div class="input-box">
          <span class="icon"><span class="material-symbols-outlined">lock</span></span>
          <input type="password" v-model="registerForm.password" required>
          <label>Senha</label>
        </div>
        <div class="remember-forgot">
          <label><input type="checkbox" required>Eu concordo com os termos & normas</label>
        </div>
        <button type="submit" class="btn">Registre-se</button>
        <div class="login-register">
          <p>Já tem uma conta?<a href="" class="register-link" @click.prevent="toggleWrapper(false)">Login</a></p>
        </div>
        <p v-if="registerError" class="error-message">{{ registerError }}</p>
        <p v-if="registerSuccess" class="success-message">{{ registerSuccess }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/user'
const authStore = useAuthStore()

const router = useRouter()

const isWrapperActive = ref(false)
const isLogging = ref(false)
const loginError = ref('')
const registerError = ref('')
const registerSuccess = ref('')

// forms
const loginForm = ref({
  username: '',
  password: ''
})

const registerForm = ref({
  username: '',
  email: '',
  password: ''
})


const toggleWrapper = (active) => {
  isWrapperActive.value = active
  if (active) {
    registerError.value = ''
    registerSuccess.value = ''
  }
}

const toggleLogin = (active) => {
  isLogging.value = active
  if (!active) {
    loginError.value = ''
  }
}

const handleLogout = async () => {
  try {
    // logout no backend
    const response = await fetch('http://localhost:5000/logout', {
      method: 'POST',
      credentials: 'include'
    })
    
    if (response.ok) {
      // limpa o frontend
      authStore.logout()

      // window.location.reload()
      user.value = null
      isAuthenticated.value = false
      
      // remove do local
      localStorage.removeItem('user')
      localStorage.removeItem('isAuthenticated')
      
    } else {
      console.error('Falha no logout no servidor')
    }
  } catch (error) {
    console.error('Erro ao fazer logout:', error)
  }
}

// login
const handleLogin = async () => {
  try {
    const response = await fetch('http://localhost:5000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: loginForm.value.username,
        password: loginForm.value.password
      }),
      credentials: 'include' // session cookies 
    })

    const data = await response.json()
    console.log(data)

    if (response.ok) {
      // Login deu certo
      toggleLogin(false);
      authStore.login(data.user);
      localStorage.setItem('user', JSON.stringify(data))
      localStorage.setItem('isAuthenticated', 'true')
      
    } else {
      loginError.value = data.error || 'Erro ao fazer login'
    }
  } catch (error) {
    loginError.value = 'Erro de conexão com o servidor'
  }
}

// registro
const handleRegister = async () => {
  try {
    const response = await fetch('http://localhost:5000/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: registerForm.value.username,
        email: registerForm.value.email,
        password: registerForm.value.password
      })
    })

    const data = await response.json()

    if (response.status === 201) {
      registerSuccess.value = data.message
      registerError.value = ''
      // limpar formulário
      registerForm.value = { username: '', email: '', password: '' }
      setTimeout(() => {
        toggleWrapper(false)
      }, 2000)
    } else {
      registerError.value = data.error || 'Erro ao registrar'
      registerSuccess.value = ''
    }
  } catch (error) {
    registerError.value = 'Erro de conexão com o servidor'
  }
}
</script>

<style lang="scss">
@import '@/assets/scss/home.scss';
</style>