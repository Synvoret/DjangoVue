// PROFILEs
import RegisterView from "@/views/Users/RegisterView.vue";
import LoginView from "@/views/Users/LoginView.vue";

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
    }
]
