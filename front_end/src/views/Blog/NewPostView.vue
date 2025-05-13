<script setup>
    import NewPost from "@/components/NewPost.vue";
    import { inject } from 'vue';


    const currentUser = inject('currentUser');
</script>

<template>
    <span><h2>New Post </h2><span>by </span><h3>{{ currentUser }}</h3></span>
    <NewPost />
</template>

<style scoped>
    h2 {
        color: blue;
        display: inline;
    }
    h3 {
        color: red;
        display: inline;
        font-style: italic;
    }
</style>
