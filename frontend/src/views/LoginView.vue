<template>
  <div class="login-page">
    <!-- HEADER -->
    <div class="top-brand">
      <div class="brand-box">Prediksi Resiko Kredit</div>
    </div>

    <!-- LOGIN CARD -->
    <div class="login-wrapper">
      <!-- LEFT -->
      <div class="login-left">
        <!-- nanti bisa ganti logo -->
        <div class="image-placeholder">
          <img :src="logo" alt="logo credit skoring" class="img-fluid" />
        </div>
      </div>

      <!-- RIGHT -->
      <div class="login-right">
        <h1 class="title">
          Selamat Datang di
          <br />
          Prediksi Resiko Kredit
        </h1>

        <p class="subtitle">
          masuk untuk mengakses sistem prediksi risiko kredit berbasis
          Artificial Intelligence.
        </p>

        <div class="form-group">
          <label> Username / Email / Nomor Telepon </label>

          <input
            v-model="login_input"
            class="form-control"
            placeholder="Masukkan username, email atau nomor telepon"
            @keyup.enter="login"
          />
        </div>

        <div class="form-group">
          <label>Password</label>

          <input
            v-model="password"
            type="password"
            class="form-control"
            placeholder="Masukkan password"
            @keyup.enter="login"
          />
        </div>

        <button class="btn-login" @click="login" :disabled="loading">
          {{ loading ? "Memproses..." : "Login" }}
        </button>

        <div class="register-link">
          Tidak Punya Akun?

          <router-link to="/register"> Buat Akun </router-link>
        </div>
      </div>
    </div>

    <!-- FOOTER -->
    <footer class="footer">
      <div>
        <h6>Credit Risk Scoring</h6>
        <p>Sistem prediksi risiko kredit berbasis Artificial Intelligence.</p>
      </div>

      <div>
        <h6>Produk</h6>
        <p>Prediksi</p>
        <p>Analisis</p>
        <p>Monitoring</p>
      </div>

      <div>
        <h6>Perusahaan</h6>
        <p>Tentang</p>
        <p>Legalitas</p>
        <p>Karir</p>
      </div>

      <div>
        <h6>Support</h6>
        <p>Dokumentasi</p>
        <p>Kontak</p>
        <p>Status</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import Swal from "sweetalert2";

import logo from "../assets/logo.jpg";

const router = useRouter();
const auth = useAuthStore();

const login_input = ref("");
const password = ref("");
const loading = ref(false);

const login = async () => {
  // ===============================
  // VALIDASI FORM
  // ===============================

  if (!login_input.value || !password.value) {
    await Swal.fire({
      icon: "warning",
      title: "Data Belum Lengkap",
      text: "Username / Email / Nomor Telepon dan Password wajib diisi.",
      confirmButtonColor: "#ffc107",
    });

    return;
  }

  try {
    loading.value = true;

    const user = await auth.login(login_input.value, password.value);

    await Swal.fire({
      icon: "success",
      title: "Login Berhasil",
      text: `Selamat datang, ${user.nama_lengkap}!`,
      timer: 1500,
      showConfirmButton: false,
    });

    switch (user.role) {
      case "super_admin":
        router.push("/admin");
        break;

      case "operator":
        router.push("/operator");
        break;

      default:
        router.push("/dashboard");
    }
  } catch (error) {
    await Swal.fire({
      icon: "error",
      title: "Login Gagal",
      text: error.response?.data?.message || "Username atau password salah.",
      confirmButtonColor: "#dc3545",
    });
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped src="../css/LoginView.css"></style>