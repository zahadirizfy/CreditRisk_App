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
            <label>Daftar sebagai</label>

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
                  value="instansi"
                  v-model="form.role"
                />

                <label class="form-check-label"> Instansi </label>
              </div>
            </div>
          </div>

          <!-- instansi -->
          <div class="form-group" v-if="form.role === 'instansi'">
            <label>Instansi</label>

            <input
              v-model="form.instansi"
              type="text"
              class="form-control"
              placeholder="Nama instansi"
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
import Swal from "sweetalert2";

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
  instansi: "",
  role: "nasabah",
});

const register = async () => {
  if (form.password !== confirmPassword.value) {
    Swal.fire({
      icon: "warning",
      title: "Password Tidak Sama",
      text: "Pastikan password dan konfirmasi password sama.",
      confirmButtonColor: "#ffc107",
    });
    return;
  }

  try {
    loading.value = true;

    const response = await api.post("/register", form);

    await Swal.fire({
      icon: "success",
      title: "Registrasi Berhasil",
      text: response.data.message,
      confirmButtonText: "Login Sekarang",
      confirmButtonColor: "#0d6efd",
    });

    router.push("/login");
  } catch (error) {
    console.log(error);

    Swal.fire({
      icon: "error",
      title: "Registrasi Gagal",
      text: error.response?.data?.message || "Terjadi kesalahan pada server.",
      confirmButtonColor: "#dc3545",
    });
  } finally {
    loading.value = false;
  }
};
</script>



<style scoped src="../css/RegisterView.css"></style>