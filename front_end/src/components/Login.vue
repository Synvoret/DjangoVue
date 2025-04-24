<script setup>
    import { ref } from 'vue';
    import { useMutation } from "@vue/apollo-composable";
    import gql from "graphql-tag";

    const username = ref('');
    const password = ref('');
    const success = ref(false);
    const loggedProfile = ref(null);

    const { mutate: loginProfile } = useMutation(
        gql`
            mutation LoginProfile($username: String!, $password: String!) {
                loginProfile(username: $username, password: $password) {
                    profile {
                        user {
                            username
                            password
                        }
                    }
                }
            }
        `);
    async function login() {
        try {
            const response = await loginProfile({
                username: username.value,
                password: password.value,
            });
            console.log(response.data)
            success.value = true;
            loggedProfile.value = response.data.loginProfile.profile
            setTimeout(() => {
                success.value = false;
            }, 5000);
            // const createdProfile = response.data.createProfile.profile;
            // console.log(createdProfile)
        } catch (error) {
            console.error("GraphQL Error:", error);
        }
    } 
</script>

<template>
    <form @submit.prevent="login">
        <div>
            <label for="username">Username: </label>
            <input type="text" v-model="username" placeholder="username" required/>
        </div>
        <div>
            <label for="password">Password: </label>
            <input type="password" v-model="password" placeholder="password" required/>
        </div>
        <button type="submit">Login</button>
    </form>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error.message }}</div>
    <div v-else-if="success">Profile logged.</div>

    <div v-if="loggedProfile">
        <h5>Welcome, <span>{{ loggedProfile.user.username }}</span></h5>
    </div>
</template>

<style scoped>
    span {
        color: green;
    }
</style>
