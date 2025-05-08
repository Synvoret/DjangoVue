<script setup>
  import { ref, provide, watch } from 'vue';
  import { RouterView } from "vue-router";
  import Header from './components/Header.vue';
  import { provideApolloClient, useQuery } from '@vue/apollo-composable';
  import apolloClient from '@/apollo';
  import gql from 'graphql-tag';

  const currentUser = ref(null);
  const isAuthenticated = ref(false);

  provide('currentUser', currentUser);
  provide('isAuthenticated', isAuthenticated);

  provideApolloClient(apolloClient);
  const { result: authResult } = useQuery(gql`
    query CheckAuth {
      checkAuth {
        isActive
        username
      }
    }
  `, null, { fetchPolicy: 'network-only' });

  watch(authResult, (newResult) => {
    if (newResult?.checkAuth?.isActive) {
      isAuthenticated.value = true;
      currentUser.value = newResult.checkAuth.username;
    } else {
      isAuthenticated.value = false;
      currentUser.value = null;
    }
  });
</script>

<template>
  <Header />
  <RouterView />
</template>
