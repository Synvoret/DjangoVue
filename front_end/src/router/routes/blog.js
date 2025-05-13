// BLOG
import AuthorPostsView from "@/views/Blog/AuthorPostsView.vue";
import AllPostsView from "@/views/Blog/AllPostsView.vue";
import PostView from "@/views/Blog/PostView.vue";
import PostsByTagView from "@/views/Blog/PostsByTagView.vue";

export default [
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
        component: () => import('@/views/Blog/NewPostView.vue'),
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
]