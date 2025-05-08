import { ApolloClient, createHttpLink, InMemoryCache } from "@apollo/client/core";

function getCookie(name) {
    let value = '; ' + document.cookie;
    let parts = value.split('; ' + name + '=');
    if (parts.length === 2) return parts.pop().split(';').shift();
    return '';
}

const httpLink = createHttpLink({
    uri: "http://127.0.0.1:8000/graphql/",
    credentials: 'include',
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'x-csrftoken': getCookie('csrftoken'),
    },
});

const apolloClient = new ApolloClient({
    link: httpLink,
    cache: new InMemoryCache(),
});

export default apolloClient;
