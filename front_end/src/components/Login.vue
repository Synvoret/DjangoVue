<script setup>
    import { ref, inject } from 'vue';
    import { useMutation } from "@vue/apollo-composable";
    import gql from "graphql-tag";

    const loggedProfile = inject('loggedProfile');

    const username = ref('');
    const password = ref('');
    const success = ref(false);
    // const loggedProfile = ref(null);

    const { mutate: LoginUser, loading, error } = useMutation(
        gql`
            mutation LoginUser($username: String!, $password: String!) {
                loginUser(username: $username, password: $password) {
                    user {
                        id
                        username
                    }
                }
            }
        `);
    async function handleAuth() {
        // LOGIN
        if (!loggedProfile.value) {
            try {
                const response = await LoginUser({
                    username: username.value,
                    password: password.value,
                });
                success.value = true;
                loggedProfile.value = response.data.loginUser.user.username;
                // setTimeout(() => {
                //     success.value = false;
                // }, 5000);
            } catch (error) {
                console.error("GraphQL Error:", error);
            }
        // LOGUT
        } else {
            loggedProfile.value = null;
            username.value = '';
            password.value = '';
        }
    }
</script>

<template>
    <form @submit.prevent="handleAuth">
        <div v-if="!loggedProfile">
            <label for="username">Username: </label>
            <input type="text" v-model="username" placeholder="username" required/>
        </div>
        <div v-else></div>

        <div v-if="!loggedProfile">
            <label for="password">Password: </label>
            <input type="password" v-model="password" placeholder="password" required/>
        </div>
        <div v-else></div>

        <button type="submit">
            {{ loggedProfile ? 'Logout' : 'Login' }}
        </button>
    </form>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error.message }}</div>
    <div v-else-if="success && loggedProfile">Profile logged.</div>
    <div v-if="loggedProfile"><h5>Welcome, <span>{{ loggedProfile }}</span></h5></div>
    <div v-else-if="loggedProfile"><h5>Bye 👋</h5></div>
</template>

<style scoped>
    span {
        color: green;
    }
</style>
