// src/router/index.js

import { createRouter, createWebHistory } from "vue-router";

import LandingView from "../views/LandingView.vue";
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import DashboardView from "../views/DashboardView.vue";
import PredictionView from "../views/PredictionView.vue";
import HistoryView from "../views/HistoryView.vue";
import ProfileView from "../views/ProfileView.vue";
import AdminDashboardView from "../views/AdminDashboardView.vue";
import OperatorDashboardView from "../views/OperatorDashboardView.vue";

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
      roles: ["nasabah", "instansi"],
    },
  },

  {
    path: "/prediction",
    component: PredictionView,
    meta: {
      requiresAuth: true,
      roles: ["nasabah", "instansi"],
    },
  },

  {
    path: "/history",
    component: HistoryView,
    meta: {
      requiresAuth: true,
      roles: ["nasabah", "instansi"],
    },
  },

  {
    path: "/profile",
    component: ProfileView,
    meta: {
      requiresAuth: true,
      roles: ["super_admin", "operator", "instansi", "nasabah"],
    },
  },

  {
    path: "/admin",
    component: AdminDashboardView,
    meta: {
      requiresAuth: true,
      roles: ["super_admin"],
    },
  },
  {
    path: "/operator",
    component: OperatorDashboardView,
    meta: {
      requiresAuth: true,
      roles: ["operator"],
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

  const user = JSON.parse(localStorage.getItem("user") || "null");

  // ==========================================
  // BELUM LOGIN
  // ==========================================

  if (to.meta.requiresAuth && !token) {
    next("/login");
    return;
  }

  // ==========================================
  // SUDAH LOGIN
  // ==========================================

  if (token && (to.path === "/login" || to.path === "/register")) {
    switch (user?.role) {
      case "super_admin":
        next("/admin");
        return;

      case "operator":
        next("/operator");
        return;

      default:
        next("/dashboard");
        return;
    }
  }

  // ==========================================
  // ROLE GUARD
  // ==========================================

  if (to.meta.roles && !to.meta.roles.includes(user?.role)) {
    switch (user?.role) {
      case "super_admin":
        next("/admin");
        break;

      case "operator":
        next("/operator");
        break;

      default:
        next("/dashboard");
        break;
    }

    return;
  }

  next();
});

export default router;
