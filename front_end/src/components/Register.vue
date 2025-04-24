<script setup>
    import { ref } from 'vue';
    import { useMutation } from "@vue/apollo-composable";
    import gql from "graphql-tag";

    const username = ref('');
    const password = ref('');
    const website = ref('');
    const bio = ref('');
    const success = ref(false);

    const { mutate: createProfile, loading, error } = useMutation(
        gql`
            mutation CreateProfile($username: String!, $password: String!, $website: String, $bio: String) {
                createProfile(username: $username, password: $password, website: $website, bio: $bio) {
                    profile {
                        user {
                            username
                            password
                        }
                        website
                        bio
                    }
                }
            }
        `);
    async function registerProfile() {
        try {
            const response = await createProfile({
                username: username.value,
                password: password.value,
                website: website.value,
                bio: bio.value,
            });
            success.value = true;
            const createdProfile = response.data.createProfile.profile;
            console.log(createdProfile)
        } catch (error) {
            console.error("GraphQL Error:", error);
        }
    } 
</script>

<template>
    <form @submit.prevent="registerProfile">
        <div>
            <label for="username">Username: </label>
            <input type="text" v-model="username" placeholder="username" required/>
        </div>
        <div>
            <label for="password">Password: </label>
            <input type="password" v-model="password" placeholder="password" required/>
        </div>
        <div>
            <label for="website">Website: </label>
            <input type="text" v-model="website" placeholder="website"/>
        </div>
        <div>
            <label for="bio">Bio: </label>
            <input type="text" v-model="bio" placeholder="bio"/>
        </div>
        <button type="submit">Register</button>
    </form>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error.message }}</div>
    <div v-else-if="success">Profile created.</div>
</template>
