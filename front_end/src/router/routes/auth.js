// PROFILEs
import RegisterView from "@/views/Users/RegisterView.vue";
import LoginView from "@/views/Users/LoginView.vue";
import UsersView from "@/views/Users/UsersView.vue";

export default [
    {
        path: "/register",
        name: "register",
        component: RegisterView,
    },
    {
        path: "/login",
        name: "login",
        component: LoginView,
    },
    {
        path: "/users",
        name: "users",
        component: UsersView,
    }
]
