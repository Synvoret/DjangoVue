<script setup>
    import Login from "@/components/Login.vue";
    import { inject } from 'vue';

    const isAuthenticated = inject('isAuthenticated');
</script>

<template>
    <h2 v-if="!isAuthenticated">Login</h2>
    <Login />
</template>

<style scoped>
    h2 {
        color: blue;
    }
</style>