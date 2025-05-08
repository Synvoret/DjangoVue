import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useMutation } from '@vue/apollo-composable';
import gql from 'graphql-tag';
import { useAuth } from './useAuth';

const LOGIN_MUTATION = gql`
    mutation LoginUser($username: String!, $password: String!) {
        loginUser(username: $username, password: $password) {
        user {
            id
            username
        }
        }
    }
`;

const LOGOUT_MUTATION = gql`
    mutation LogoutUser {
        logoutUser {
        success
        }
    }
`;

export function useHandleAuth() {
    const { currentUser, isAuthenticated } = useAuth();
    const username = ref('');
    const password = ref('');
    const success = ref(false);
    const router = useRouter();

    const { mutate: LoginUser, loading, error } = useMutation(LOGIN_MUTATION);
    const { mutate: LogoutUser } = useMutation(LOGOUT_MUTATION);

    async function login() {
        try {
        const response = await LoginUser({
            username: username.value,
            password: password.value,
        });
        const user = response?.data?.loginUser?.user;
        if (user) {
            currentUser.value = user.username;
            isAuthenticated.value = true;
            success.value = true;
        }
        } catch (err) {
        console.error('GraphQL Login Error:', err);
        }
    }

    async function logout() {
        try {
        await LogoutUser();
        } catch (err) {
        console.error('GraphQL Logout Error:', err);
        } finally {
        currentUser.value = null;
        isAuthenticated.value = false;
        username.value = '';
        password.value = '';
        success.value = false;
        router.push('/login');
        }
    }

    return {
        login,
        logout,
        username,
        password,
        success,
        loading,
        error,
    };
}
