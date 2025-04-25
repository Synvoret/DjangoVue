<script setup>
    import Login from "../components/Login.vue";
    import { ref, inject } from 'vue';

    const loggedProfile = inject('loggedProfile');
</script>

<template>
    <h2>{{ loggedProfile ? 'Logout' : 'Login' }}</h2>
    <Login />
</template>

<style scoped>
    h2 {
        color: blue;
    }
</style>