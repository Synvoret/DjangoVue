<script setup>

    import { useAuth } from '@/hooks/useAuth';
    import { useHandleAuth } from '@/hooks/useHandleAuth';
    import { RouterLink } from 'vue-router';

    const { currentUser, isAuthenticated } = useAuth();
    const { logout } = useHandleAuth();
</script>

<template>
    <nav>
        <RouterLink to="/">Posts</RouterLink>
        <RouterLink to="/items">Items</RouterLink>
        <RouterLink v-if="!isAuthenticated" to="/login">Login</RouterLink>
        <a v-else href="#" @click.prevent="logout">
            Logout
            <span class="username">{{ currentUser }}</span>
        </a>
        <RouterLink to="/register" v-if="!isAuthenticated">Register</RouterLink>
    </nav>
</template>

<style scoped>
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
