import { inject } from 'vue';

export function useAuth() {
    const isAuthenticated = inject('isAuthenticated');
    const currentUser = inject('currentUser');

    if (!isAuthenticated || !currentUser) {
        throw new Error('Auth context not provided');
    }

    return { isAuthenticated, currentUser };
}
