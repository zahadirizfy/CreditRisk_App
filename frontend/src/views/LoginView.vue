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

        <div class="login-options">
          <div>
            <input type="checkbox" />
            Ingat saya
          </div>
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

import logo from "../assets/logo.jpg";

const router = useRouter();
const auth = useAuthStore();

const login_input = ref("");
const password = ref("");
const loading = ref(false);

const login = async () => {
  if (!login_input.value || !password.value) {
    alert("Username / Email / Nomor Telepon dan Password wajib diisi");
    return;
  }

  try {
    loading.value = true;

    await auth.login(login_input.value, password.value);

    router.push("/dashboard");
  } catch (error) {
    alert(error.response?.data?.message || "Login gagal");
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 20px;
}

.top-brand {
  margin-bottom: 20px;
}

.brand-box {
  display: inline-block;
  background: #e9ecef;
  padding: 10px 20px;
  font-weight: 600;
  border-radius: 8px;
}

.login-wrapper {
  background: white;
  border-radius: 12px;
  padding: 30px;
  display: flex;
  gap: 40px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.login-left {
  flex: 1;
}

.image-placeholder {
  width: 100%;
  height: 450px;
  border: 2px solid #ccc;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.image-placeholder img {
  max-width: 100%;
  max-height: 100%;
}

.login-right {
  flex: 1;
}

.title {
  font-weight: 700;
  margin-bottom: 10px;
}

.subtitle {
  color: #666;
  margin-bottom: 25px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  margin-bottom: 6px;
  display: block;
  font-size: 14px;
  font-weight: 500;
}

.login-options {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  font-size: 14px;
}

.btn-login {
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 10px;
  background: #0d6efd;
  color: white;
  font-weight: 600;
}

.btn-login:hover {
  background: #0b5ed7;
}

.register-link {
  text-align: center;
  margin-top: 15px;
}

.footer {
  margin-top: 40px;
  background: #e9ecef;
  padding: 25px;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.footer h6 {
  font-weight: 700;
}

.footer p {
  margin: 4px 0;
  font-size: 14px;
}

@media (max-width: 768px) {
  .login-wrapper {
    flex-direction: column;
  }

  .footer {
    grid-template-columns: 1fr;
  }
}
</style>
