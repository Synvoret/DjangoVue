<script setup>
    import { useAuth } from '@/hooks/useAuth';
    import { useHandleAuth } from '@/hooks/useHandleAuth';
    import CrudButton from "@/components/common/CrudButton.vue";

    const { isAuthenticated, currentUser } = useAuth();
    const {
        login,
        username,
        password,
        success,
        loading,
        error,
    } = useHandleAuth();
</script>

<template>
    <form @submit.prevent="login" v-if="!isAuthenticated">
        <div class="form-group">
            <label for="username">Username: </label>
            <input type="text" v-model="username" placeholder="username" required />
        </div>
        <div class="form-group">
            <label for="password">Password: </label>
            <input type="password" v-model="password" placeholder="password" required />
        </div>
        <div class="button-container">
            <CrudButton label="Login" buttonClass="login" @click="login"/>
        </div>
    </form>

    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error.message }}</div>
    <div v-else-if="success && isAuthenticated">Profile logged.</div>
    <div v-if="isAuthenticated">
        <h5>Welcome, <span>{{ currentUser }}</span></h5>
    </div>
</template>

<style scoped>
    span {
        color: green;
    }
</style>
