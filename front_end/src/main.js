import './assets/main.css'

import { createApp, provide, h } from 'vue';
import App from './App.vue';
import router from './router';
import {
    ApolloClient,
    createHttpLink,
    InMemoryCache,
} from "@apollo/client/core";
import { DefaultApolloClient } from "@vue/apollo-composable";

const httpLink = createHttpLink({
    uri: "http://localhost:8000/graphql/",
    // uri: "http://127.0.0.1:8000/graphql/",
    credentials: 'include', // for cookies
    headers: {
        'content-type': 'application/json',
        'x-csrftoken': getCookie('csrftoken'),
    },
});

function getCookie(name) {
    let value = '; ' + document.cookie;
    let parts = value.split('; ' + name + '=');
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
}

const cache = new InMemoryCache();

const apolloClient = new ApolloClient({
    link: httpLink,
    cache,
});

const app = createApp({
    setup() {
        provide(DefaultApolloClient, apolloClient);
    },
    render: () => h(App),
});

app.use(router);

app.mount('#app')
