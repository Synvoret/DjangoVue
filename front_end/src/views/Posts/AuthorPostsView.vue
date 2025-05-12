<script setup>
    import { inject, computed } from 'vue';
    import PostList from "@/components/PostList.vue";
    import { useRoute } from "vue-router";
    import { useQuery } from "@vue/apollo-composable";
    import gql from "graphql-tag";
    import router from '@/router';
    import CrudButton from "@/components/common/CrudButton.vue";

    const route = useRoute();
    const currentUser = inject('currentUser');
    const isAuthenticated = inject('isAuthenticated');
    const username = route.params.username;
    const { result, loading, error } = useQuery(gql`
        query {
            authorByUsername(
                username: "${username}"
            ) {
                website
                bio
                user {
                    firstName
                    lastName
                    username
                }
                postSet {
                    title
                    slug
                }
            }
        }
    `);
    const addNewPost = () => {
        router.push({ name: "newPost" });
    };
    const isOwnProfile = computed(() => {
        return isAuthenticated && currentUser.value === username;
    })
</script>

<template>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error.message }}</div>
    <section v-else :set="author = result.authorByUsername">
        <span>
            <p>Author: </p>
            <h2>{{ author.user.username }}</h2>
        </span>
        <template v-if="author.user.firstName && author.user.lastName">
            <h3>{{ author.user.firstName }} {{ author.user.lastName }}</h3>
        </template>
        <p v-if="author.bio">
            {{ author.bio }}
            <template v-if="author.website">
                Learn more about {{ author.user.username }} on their
                <a :href="author.website">website</a>.
            </template>
        </p>
        <h3>Posts</h3>
        <PostList v-if="author.postSet" :posts="author.postSet" :showAuthor="false" />
        <p v-else>The author hasn't posted yet.</p>
        <div v-if="isOwnProfile">
            <CrudButton label="Add new Post" buttonClass="create" :action="addNewPost"/>
        </div>
    </section>
</template>

<style scoped>
    h2 {
        color: red;
        display: inline;
        font-style: italic;
    }
    p {
        display: inline;
    }
</style>