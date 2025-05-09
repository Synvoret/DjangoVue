import { createRouter, createWebHistory } from "vue-router";
// BLOG
import AuthorPostsView from "@/views/Posts/AuthorPostsView.vue";
import AllPostsView from "@/views/Posts/AllPostsView.vue";
import PostView from "@/views/Posts/PostView.vue";
import PostsByTagView from "@/views/Posts/PostsByTagView.vue";
// CRUD
import ItemListView from "@/views/Items/ItemListView.vue";
// PROFILEs
import RegisterView from "@/views/Users/RegisterView.vue";
import LoginView from "@/views/Users/LoginView.vue";

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
      component: AuthorPostsView,
    },
    // CRUD (posts)
    {
      path: "/author/:username/newPost",
      name: "newPost",
      component: () => import('@/views/Posts/NewPostView.vue'),
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
      component: ItemListView,
    },
    // PROFILEs
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
  ],
});

export default router;
