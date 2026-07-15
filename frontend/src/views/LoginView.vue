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

        <div class="forgot-password-link">
          <a href="#" @click.prevent="openForgotModal">Lupa Password?</a>
        </div>

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

  <div v-if="showForgotModal" class="modal-overlay">
    <div class="modal-content">
      <button class="close-btn" @click="closeForgotModal">&times;</button>

      <div v-if="forgotStep === 1">
        <h3 class="modal-title">Lupa Password</h3>
        <p class="modal-subtitle">
          Masukkan email Anda yang terdaftar untuk menerima kode OTP.
        </p>
        <div class="form-group">
          <label>Email Terdaftar</label>
          <input
            v-model="forgotEmail"
            type="email"
            class="form-control"
            placeholder="user@gmail.com"
          />
        </div>
        <button class="login-btn" @click="requestOtp" :disabled="isSubmitting">
          {{ isSubmitting ? "Mengirim..." : "Kirim Kode OTP" }}
        </button>
      </div>

      <div v-if="forgotStep === 2">
        <h3 class="modal-title">Verifikasi Kode</h3>
        <p class="modal-subtitle">
          Masukkan 6 digit kode OTP yang telah dikirim ke
          <b>{{ forgotEmail }}</b>
        </p>
        <div class="form-group">
          <label>Kode OTP</label>
          <input
            v-model="forgotOtp"
            type="text"
            class="form-control"
            placeholder="123456"
            maxlength="6"
          />
        </div>
        <button class="login-btn" @click="goToNewPasswordStep">Lanjut</button>
      </div>

      <div v-if="forgotStep === 3">
        <h3 class="modal-title">Buat Password Baru</h3>
        <p class="modal-subtitle">Silakan buat password baru Anda.</p>
        <div class="form-group">
          <label>Password Baru</label>
          <input
            v-model="newPassword"
            type="password"
            class="form-control"
            placeholder="Minimal 8 karakter"
          />
        </div>
        <div class="form-group">
          <label>Konfirmasi Password</label>
          <input
            v-model="confirmPassword"
            type="password"
            class="form-control"
            placeholder="Ketik ulang password baru"
          />
        </div>
        <button
          class="login-btn"
          @click="submitResetPassword"
          :disabled="isSubmitting"
        >
          {{ isSubmitting ? "Menyimpan..." : "Simpan Password Baru" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import Swal from "sweetalert2";
import axios from "axios";

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

// STATE LUPA PASSWORD
const showForgotModal = ref(false);
const forgotStep = ref(1); // 1: Email, 2: OTP, 3: Password Baru
const forgotEmail = ref("");
const forgotOtp = ref("");
const newPassword = ref("");
const confirmPassword = ref("");
const isSubmitting = ref(false);

// ==========================================
// FUNGSI LUPA PASSWORD
// ==========================================

const openForgotModal = () => {
  showForgotModal.value = true;
  forgotStep.value = 1;
  forgotEmail.value = "";
  forgotOtp.value = "";
  newPassword.value = "";
  confirmPassword.value = "";
};

const closeForgotModal = () => {
  showForgotModal.value = false;
};

// Tahap 1: Minta Kode OTP
const requestOtp = async () => {
  if (!forgotEmail.value) {
    Swal.fire({ icon: "warning", text: "Email wajib diisi!" });
    return;
  }

  isSubmitting.value = true;
  try {
    // Sesuaikan URL Backend Anda
    const response = await axios.post(
      "http://localhost:5000/api/forgot-password",
      { email: forgotEmail.value },
    );

    // Simulasi sukses API:
    Swal.fire({
      icon: "success",
      title: "OTP Dikirim!",
      text: "Silakan cek inbox/spam email Anda.",
      timer: 2000,
      showConfirmButton: false,
    });

    // Pindah ke step 2
    forgotStep.value = 2;
  } catch (error) {
    Swal.fire({
      icon: "error",
      title: "Gagal",
      text:
        error.response?.data?.message ||
        "Terjadi kesalahan saat mengirim email.",
    });
  } finally {
    isSubmitting.value = false;
  }
};

// Tahap 2: Lanjut ke buat password baru (Karena verifikasi OTP sekalian dengan input password di backend)
const goToNewPasswordStep = () => {
  if (!forgotOtp.value) {
    Swal.fire({ icon: "warning", text: "Kode OTP wajib diisi!" });
    return;
  }
  forgotStep.value = 3;
};

// Tahap 3: Submit Password Baru
const submitResetPassword = async () => {
  if (!newPassword.value || !confirmPassword.value) {
    Swal.fire({ icon: "warning", text: "Semua kolom password wajib diisi!" });
    return;
  }

  if (newPassword.value !== confirmPassword.value) {
    Swal.fire({ icon: "error", text: "Konfirmasi password tidak cocok!" });
    return;
  }

  isSubmitting.value = true;
  try {
    // Sesuaikan URL Backend Anda

    const response = await axios.post(
      "http://localhost:5000/api/reset-password",
      {
        email: forgotEmail.value,
        otp_code: forgotOtp.value,
        new_password: newPassword.value,
      },
    );

    // Simulasi sukses:
    await Swal.fire({
      icon: "success",
      title: "Berhasil!",
      text: "Password Anda berhasil direset. Silakan login.",
    });

    // Tutup modal
    closeForgotModal();
  } catch (error) {
    Swal.fire({
      icon: "error",
      title: "Gagal",
      text:
        error.response?.data?.message ||
        "Gagal mereset password atau OTP salah.",
    });
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped src="../css/LoginView.css"></style>
