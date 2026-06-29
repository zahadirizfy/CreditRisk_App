// src/router/index.js

import { createRouter, createWebHistory } from "vue-router";

import LandingView from "../views/LandingView.vue";
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import DashboardView from "../views/DashboardView.vue";
import PredictionView from "../views/PredictionView.vue";
import HistoryView from "../views/HistoryView.vue";
import ProfileView from "../views/ProfileView.vue";

const routes = [
  {
    path: "/",
    component: LandingView,
  },

  {
    path: "/login",
    component: LoginView,
  },

  {
    path: "/register",
    component: RegisterView,
  },

  {
    path: "/dashboard",
    component: DashboardView,
    meta: {
      requiresAuth: true,
    },
  },

  {
    path: "/prediction",
    component: PredictionView,
    meta: {
      requiresAuth: true,
    },
  },

  {
    path: "/history",
    component: HistoryView,
    meta: {
      requiresAuth: true,
    },
  },

  {
    path: "/profile",
    component: ProfileView,
    meta: {
      requiresAuth: true,
    },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// ==========================================
// ROUTE GUARD
// ==========================================

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("token");

  // Belum login
  if (to.meta.requiresAuth && !token) {
    next("/login");
    return;
  }

  // Sudah login
  if (token && (to.path === "/login" || to.path === "/register")) {
    next("/dashboard");
    return;
  }

  next();
});

export default router;
