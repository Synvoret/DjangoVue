import { createRouter, createWebHistory } from "vue-router";

import authRoutes from "@/router/routes/auth.js";
import blogRoutes from '@/router/routes/blog.js';
import crudRoutes from "@/router/routes/crud.js";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // PROFILEs
    ...authRoutes,
    // BLOG
    ...blogRoutes,
    // CRUD
    ...crudRoutes,
  ],
});

export default router;
