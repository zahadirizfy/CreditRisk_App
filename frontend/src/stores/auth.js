import { defineStore } from "pinia";
import api from "../services/api";

export const useAuthStore = defineStore("auth", {

    state: () => ({
        token: localStorage.getItem("token") || null,

        user: JSON.parse(
            localStorage.getItem("user")
        ) || null
    }),

    getters: {

        isAuthenticated: (state) =>
            !!state.token

    },

    actions: {

        // ==========================================
        // LOGIN
        // ==========================================

        async login(
            login_input,
            password
        ) {

            const response = await api.post(
                "/login",
                {
                    login_input,
                    password
                }
            );

            this.token =
                response.data.token;

            this.user =
                response.data.user;

            localStorage.setItem(
                "token",
                this.token
            );

            localStorage.setItem(
                "user",
                JSON.stringify(
                    this.user
                )
            );

            return response;
        },

        // ==========================================
        // LOGOUT
        // ==========================================

        logout() {

            this.token = null;
            this.user = null;

            localStorage.removeItem(
                "token"
            );

            localStorage.removeItem(
                "user"
            );

        },

        // ==========================================
        // LOAD USER
        // ==========================================

        loadUser() {

            const token =
                localStorage.getItem(
                    "token"
                );

            const user =
                localStorage.getItem(
                    "user"
                );

            if (token) {

                this.token = token;
            }

            if (user) {

                this.user =
                    JSON.parse(user);
            }

        }

    }

});