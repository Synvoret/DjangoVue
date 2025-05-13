<script setup>
    import { ref } from 'vue';
    import { useMutation } from "@vue/apollo-composable";
    import gql from "graphql-tag";
    import CrudButton from "@/components/common/CrudButton.vue";

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
        <div class="form-group">
            <label for="title">*Title: </label>
            <input type="text" v-model="title" placeholder="title" required/>
        </div>
        <div class="form-group">
            <label for="slug">*Slug: </label>
            <input type="text" v-model="slug" placeholder="slug" required/>
        </div>
        <div class="form-group">
            <label for="body">*Text: </label>
            <textarea v-model="body" placeholder="body"></textarea>
        </div>
        <div class="form-group">
            <label class="required">* - required</label>
        </div>
        <div class="button-container">
            <CrudButton label="Save Post" buttonClass="create" type="submit"/>
        </div>
    </form>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error.message }}</div>
    <div v-else-if="success">Post "{{ title }}" created.</div>
</template>
