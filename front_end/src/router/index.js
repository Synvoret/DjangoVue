import { createRouter, createWebHistory } from "vue-router";
import AuthorView from "../views/AuthorView.vue";
import AllPostsView from "../views/AllPostsView.vue";
import PostView from "../views/PostView.vue";
import PostsByTagView from "../views/PostsByTagView.vue";
// CRUD
import ItemList from "../views/ItemList.vue";
// PROFILEs
import RegisterView from "../views/RegisterView.vue";
import LoginView from "../views/LoginView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "posts",
      component: AllPostsView,
    },
    {
      path: "/author/:username",
      name: "author",
      component: AuthorView,
    },
    {
      path: "/post/:slug",
      name: "post",
      component: PostView,
    },
    {
      path: "/tag/:tag",
      name: "tag",
      component: PostsByTagView,
    },
    // CRUD
    {
      path: "/items",
      name: "items",
      component: ItemList,
    },
    // PROFILEs
    {
      path: "/register",
      name: "register",
      component: RegisterView
    },
    {
      path: "/login",
      name: "login",
      component: LoginView
    }
  ],
});

export default router;