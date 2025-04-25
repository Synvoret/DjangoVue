<script setup>
  import { provide, ref } from 'vue'; 
  import { RouterLink, RouterView } from "vue-router";

  const loggedProfile = ref(null);
  provide('loggedProfile', loggedProfile);
</script>

<template>
  <header>
    <div class="wrapper">
      <h1>Blog</h1>
      <nav>
        <RouterLink to="/">Posts</RouterLink>
        <RouterLink to="/items">Items</RouterLink>
        <RouterLink :to="loggedProfile ? '/logout' : '/login'">{{ loggedProfile ? 'Logout' : 'Login'}} <span class="username" v-if="loggedProfile">{{ loggedProfile }}</span></RouterLink>
        <RouterLink to="/register">Register</RouterLink>
      </nav>
    </div>
  </header>

  <div><RouterView /></div>

</template>

<!-- ... -->

<style scoped>
  h1 {
    text-align: center;
    font-weight: bold;
    margin-bottom: 1rem;
  }
  header {
    border-bottom: 1px solid #ccc;
    margin-bottom: 1rem;
  }
  nav {
    text-align: center;
    margin: 1rem 0;
  }
  nav a {
    padding: 0.5rem;
  }
  span.username {
    font-style: italic;
    font-size: 12px;
    vertical-align: super;
  }
</style>
