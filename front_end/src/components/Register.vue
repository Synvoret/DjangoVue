<script setup>
    import { ref } from 'vue';
    import { useMutation } from "@vue/apollo-composable";
    import gql from "graphql-tag";
    import CrudButton from "@/components/common/CrudButton.vue";

    const username = ref('');
    const password = ref('');
    const email = ref('');
    const website = ref('');
    const bio = ref('');
    const success = ref(false);

    const { mutate: CreateProfile, loading, error } = useMutation(
        gql`
            mutation CreateProfile($username: String!, $password: String!, $email: String, $website: String, $bio: String) {
                createProfile(username: $username, password: $password, email: $email, website: $website, bio: $bio) {
                    user {
                        id
                        user {
                            username
                            email
                        }
                        website
                        bio
                    }
                }
            }
        `);
    async function registerProfile() {
        try {
            const response = await CreateProfile({
                username: username.value,
                password: password.value,
                email: email.value,
                website: website.value,
                bio: bio.value,
            });
            success.value = true;
            const createdProfile = response.data.createProfile.user.user.username;
            // console.log(createdProfile)
        } catch (error) {
            console.error("GraphQL Error:", error);
        }
    } 
</script>

<template>
    <form @submit.prevent="registerProfile">
        <div class="form-group">
            <label for="username">*Username: </label>
            <input type="text" v-model="username" placeholder="username" required/>
        </div>
        <div class="form-group">
            <label for="password">*Password: </label>
            <input type="password" v-model="password" placeholder="password" required/>
        </div>
        <div class="form-group">
            <label for="email">*Email: </label>
            <input type="email" v-model="email" placeholder="email" required/>
        </div>
        <div class="form-group">
            <label for="website">Website: </label>
            <input type="text" v-model="website" placeholder="website"/>
        </div>
        <div class="form-group">
            <label for="bio">Bio: </label>
            <input type="text" v-model="bio" placeholder="bio"/>
        </div>
        <div class="form-group">
            <label class="required">* - required</label>
        </div>
        <div class="button-container">
            <CrudButton type="submit" label="Register" buttonClass="register"/>
        </div>
    </form>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error.message }}</div>
    <div v-else-if="success">Profile "{{ username }}" created.</div>
</template>
