<script setup>
    import { inject, computed } from "vue";
    import PostList from "@/components/PostList.vue";
    import { useQuery } from "@vue/apollo-composable";
    import gql from "graphql-tag";
    import router from '@/router';
    import CrudButton from "@/components/common/CrudButton.vue";

    const currentUser = inject('currentUser');

    const { result, loading, error } = useQuery(gql`
        query {
            allPosts {
                title
                slug
                author {
                    user {
                        username
                        firstName
                        lastName
                    }
                }
            }
        }
    `);
    const usersWithPosts = computed(() => {
        if (!result.value || !result.value.allPosts) return [];
        const names = result.value.allPosts.map(post => post.author?.user?.username).filter(Boolean);
        return [...new Set(names)];
    });

    const addNewPost = () => {
        router.push({ name: "newPost", params: { username: currentUser } });
    };
</script>

<template>
    <h2>Recent Posts</h2>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error" class="warn">{{ error.message }}</div>
    <PostList v-else :posts="result.allPosts" />
    <div v-if="currentUser && !usersWithPosts.includes(currentUser)">
        <span>{{ currentUser }} -> </span>
        <CrudButton label="Add first Post?" buttonClass="create" :action="addNewPost"/>
    </div>
</template>

<style scoped>
    h2 {
        color: blue;
    }
</style>