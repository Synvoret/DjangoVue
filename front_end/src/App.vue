<script setup>
  import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  <header>
    <div class="wrapper">
      <h1>Blog</h1>
      <nav>
        <RouterLink to="/">Posts</RouterLink>
        <RouterLink to="/items">Items</RouterLink>
        <RouterLink to="/login">Login</RouterLink>
        <routerLink to="/register">Register</routerLink>
        <!-- Remove the links to 'author', 'post', and 'tag' -->
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
</style>
