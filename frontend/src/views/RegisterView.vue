<template>
  <div class="register-page">
    <!-- HEADER -->
    <div class="top-brand">
      <div class="brand-box">Prediksi Resiko Kredit</div>
    </div>

    <!-- REGISTER CARD -->
    <div class="register-wrapper">
      <!-- LEFT -->
      <div class="register-left">
        <div class="image-placeholder">
          <img :src="logo" alt="Logo" class="img-fluid" />
        </div>
      </div>

      <!-- RIGHT -->
      <div class="register-right">
        <h1 class="title">Buat Akun Baru</h1>

        <p class="subtitle">
          Daftar untuk membuat akun baru dan mulai menggunakan sistem prediksi
          risiko kredit berbasis Artificial Intelligence.
        </p>

        <form @submit.prevent="register">
          <!-- NAMA -->
          <div class="form-group">
            <label>Nama Lengkap</label>

            <input
              v-model="form.nama_lengkap"
              type="text"
              class="form-control"
              placeholder="Masukkan nama lengkap"
              required
            />
          </div>

          <!-- EMAIL + PHONE -->
          <div class="row">
            <div class="col-md-6 mb-3">
              <label>Email</label>

              <input
                v-model="form.email"
                type="email"
                class="form-control"
                placeholder="email@gmail.com"
                required
              />
            </div>

            <div class="col-md-6 mb-3">
              <label>Nomor HP</label>

              <input
                v-model="form.nomor_telepon"
                type="text"
                class="form-control"
                placeholder="08xxxxxxxxxx"
              />
            </div>
          </div>

          <!-- USERNAME -->
          <div class="form-group">
            <label>Username</label>

            <input
              v-model="form.username"
              type="text"
              class="form-control"
              placeholder="Masukkan username"
              required
            />
          </div>

          <!-- ROLE -->
          <div class="form-group">
            <label>Role</label>

            <div class="d-flex gap-4 mt-2">
              <div class="form-check">
                <input
                  class="form-check-input"
                  type="radio"
                  value="nasabah"
                  v-model="form.role"
                />

                <label class="form-check-label"> Nasabah </label>
              </div>

              <div class="form-check">
                <input
                  class="form-check-input"
                  type="radio"
                  value="admin_bank"
                  v-model="form.role"
                />

                <label class="form-check-label"> Bank/Koperasi </label>
              </div>
            </div>
          </div>

          <!-- INSTITUSI -->
          <div class="form-group" v-if="form.role === 'admin_bank'">
            <label>Institusi</label>

            <input
              v-model="form.institusi"
              type="text"
              class="form-control"
              placeholder="Nama Bank / Koperasi"
            />
          </div>

          <!-- PASSWORD -->
          <div class="form-group">
            <label>Password</label>

            <input
              v-model="form.password"
              type="password"
              class="form-control"
              placeholder="Masukkan password"
              required
            />

            <small class="text-muted"> Gunakan minimal 8 karakter </small>
          </div>

          <!-- CONFIRM PASSWORD -->
          <div class="form-group">
            <label>Confirm Password</label>

            <input
              v-model="confirmPassword"
              type="password"
              class="form-control"
              placeholder="Masukkan ulang password"
              required
            />
          </div>

          <button type="submit" class="btn-register" :disabled="loading">
            {{ loading ? "Memproses..." : "Daftar" }}
          </button>
        </form>

        <div class="login-link">
          Sudah punya akun?

          <router-link to="/login"> Masuk </router-link>
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
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";

import logo from "../assets/logo.jpg";

const router = useRouter();

const loading = ref(false);

const confirmPassword = ref("");

const form = reactive({
  username: "",
  email: "",
  password: "",
  nama_lengkap: "",
  nomor_telepon: "",
  institusi: "",
  role: "nasabah",
});

const register = async () => {
  if (form.password !== confirmPassword.value) {
    alert("Password dan Konfirmasi Password tidak sama");
    return;
  }

  try {
    loading.value = true;

    const response = await api.post("/register", form);

    alert(response.data.message);

    router.push("/login");
  } catch (error) {
    console.log(error);

    alert(error.response?.data?.message || "Registrasi gagal");
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.register-page {
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
  border-radius: 8px;
  font-weight: 600;
}

.register-wrapper {
  background: white;
  border-radius: 12px;
  padding: 30px;
  display: flex;
  gap: 40px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.register-left {
  flex: 1;
}

.image-placeholder {
  width: 100%;
  height: 650px;
  border: 2px solid #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.image-placeholder img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.register-right {
  flex: 1;
}

.title {
  font-weight: 700;
  margin-bottom: 8px;
}

.subtitle {
  color: #666;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 500;
}

.btn-register {
  width: 100%;
  border: none;
  border-radius: 10px;
  background: #0d6efd;
  color: white;
  padding: 12px;
  font-weight: 600;
  margin-top: 10px;
}

.btn-register:hover {
  background: #0b5ed7;
}

.login-link {
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
  .register-wrapper {
    flex-direction: column;
  }

  .image-placeholder {
    height: 250px;
  }

  .footer {
    grid-template-columns: 1fr;
  }
}
</style>
