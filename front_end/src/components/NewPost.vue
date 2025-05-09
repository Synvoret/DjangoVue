<script setup>
    import { ref } from 'vue';
    import { useMutation } from "@vue/apollo-composable";
    import gql from "graphql-tag";

    const title = ref('');
    const slug = ref('');
    const body = ref('');
    const success = ref(false);

    const { mutate: CreatePost, loading, error } = useMutation(
        gql`
            mutation CreatePost($title: String!, $slug: String!, $body: String!) {
                createPost(title: $title, slug: $slug, body: $body) {
                    post {
                        id
                        title
                        slug
                        body
                    }
                }
            }
        `);
    async function addNewPost() {
        try {
            const response = await CreatePost({
                title: title.value,
                slug: slug.value,
                body: body.value,
            });
            success.value = true;
        } catch (error) {
            console.error("GraphQL Error:", error);
        }
    } 
</script>

<template>
    <form @submit.prevent="addNewPost">
        <div>
            <label for="title">*Title: </label>
            <input type="text" v-model="title" placeholder="title" required/>
        </div>
        <div>
            <label for="slug">*Slug: </label>
            <input type="text" v-model="slug" placeholder="slug" required/>
        </div>
        <div>
            <label for="body">*Text: </label>
            <textarea v-model="body" rows="10" placeholder="body"></textarea>
        </div>
        <div><label class="required">* - required</label></div>
        <button type="submit">Save Post</button>
    </form>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error.message }}</div>
    <div v-else-if="success">Post "{{ title }}" created.</div>
</template>

<style scoped>
    label.required {
        font-size: 12px;
        font-style: italic;
    }
</style>