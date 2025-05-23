<script setup>
    import { ref, computed } from 'vue';
    import { useQuery } from '@vue/apollo-composable';
    import CrudButton from '@/components/common/CrudButton.vue';

    import gql from 'graphql-tag';

    const { result, loading, error } = useQuery(gql`
        query {
            myUser {
                id
                username
                password
                email
                profile {
                    website
                    bio
                }
            }
        }
    `, null, {
        fetchPolicy: 'network-only'
    });

    const myUser = computed(() => result.value?.myUser);
    console.log(myUser)

    function edit() {
        console.log('Edit profile')
    }
</script>

<template>
    <div>
        <div v-if="myUser">
            <p>Profile: {{ myUser.username }}</p>
            <p>Email: {{ myUser.email }}</p>
            <p>Website: {{ myUser.profile.website }}</p>
            <p>Bio: {{ myUser.profile.bio }}</p>
            <div class="button-container">
                <CrudButton label="Edit" buttonClass="edit" @click="edit"/>
            </div>
        </div>
        
        <div v-else>
            <p>Loading...</p>
        </div>
    </div>
</template>



