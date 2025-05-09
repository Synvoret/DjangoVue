<script setup>
    import ItemList from "@/components/ItemList.vue";
    import { useQuery } from "@vue/apollo-composable";
    import gql from "graphql-tag";

    const { result, loading, error, refetch } = useQuery(
        gql`
            query {
                items {
                    id
                    name
                    description
                    author {
                        user {
                            username
                        }
                    }
                }
            }
        `);
</script>

<template>
    <h2>Item List</h2>
    <p v-if="loading">Loading...</p>
    <p v-else-if="error" class="warn">{{ error.message }}</p>
    <ItemList v-else :items="result.items" :refetch="refetch"/>
</template>

<style scoped>
    h2 {
        color: blue;
    }
</style>