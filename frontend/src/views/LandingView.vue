<template>
  <div class="landing-page">
    <!-- ================= NAVBAR ================= -->

    <nav class="navbar navbar-dark bg-dark shadow-sm">
      <div class="container-fluid px-4">
        <div class="navbar-brand fw-bold">Credit Risk Prediction</div>

        <router-link to="/login" class="btn btn-outline-light">
          Login
        </router-link>
      </div>
    </nav>

    <!-- ================= HERO ================= -->

    <section class="hero-section container-fluid">
      <div class="row g-4 align-items-center">
        <!-- ================= LEFT ================= -->

        <div class="col-lg-8">
          <div class="hero-card">
            <h1 class="display-4 fw-bold mb-3">Selamat Datang</h1>

            <p class="text-muted mb-4">
              Sistem Prediksi Risiko Kredit berbasis Machine Learning
              menggunakan metode Logistic Regression dan K-Nearest Neighbor
              (KNN).
            </p>

            <div class="row g-3">
              <!-- IMAGE -->

              <div class="col-md-7">
                <div class="image-box">
                  <!-- nanti diganti gambar -->
                </div>
              </div>

              <!-- INFO -->

              <div class="col-md-5">
                <div class="mini-card">
                  <small class="text-muted">
                    Langkah {{ currentStep }} dari 3
                  </small>

                  <h5 class="mt-2">
                    {{ currentData.title }}
                  </h5>

                  <p>
                    {{ currentData.description }}
                  </p>
                </div>

                <div class="mini-card mt-3">
                  <h6>Informasi</h6>

                  <p class="mb-0">
                    Gunakan panel di sebelah kanan untuk mengenal alur kerja
                    sistem.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ================= RIGHT ================= -->

        <div class="col-lg-4">
          <div class="onboarding-card">
            <small class="text-muted"> Langkah </small>

            <h5>{{ currentStep }} / 3</h5>

            <h2 class="fw-bold mt-3">
              {{ currentData.title }}
            </h2>

            <p class="mt-3">
              {{ currentData.description }}
            </p>

            <ul class="mt-4">
              <li v-for="item in currentData.points" :key="item">
                {{ item }}
              </li>
            </ul>

            <div class="d-flex justify-content-between mt-5">
              <button
                class="btn btn-outline-secondary"
                @click="prevStep"
                :disabled="currentStep === 1"
              >
                Kembali
              </button>

              <button
                v-if="currentStep < 3"
                class="btn btn-primary"
                @click="nextStep"
              >
                Selanjutnya
              </button>

              <button v-else class="btn btn-success" @click="goLogin">
                Mulai
              </button>
            </div>

            <div class="text-center mt-4">
              <button
                v-for="n in 3"
                :key="n"
                class="step-btn"
                :class="{ active: n === currentStep }"
                @click="goStep(n)"
              >
                {{ n }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ================= DATA ML ================= -->

    <section class="content-section container-fluid">
      <div class="row align-items-center g-4">
        <div class="col-lg-7">
          <h2 class="fw-bold">Data dan Machine Learning</h2>

          <p class="text-muted mt-3">
            Sistem memanfaatkan data historis calon nasabah sebagai dasar
            analisis. Data diproses menggunakan Logistic Regression dan
            K-Nearest Neighbor (KNN) untuk menghasilkan keputusan yang lebih
            objektif.
          </p>

          <div class="row mt-4">
            <div class="col-md-6">
              <ul>
                <li>Identitas Nasabah</li>
                <li>Data Keuangan</li>
                <li>Riwayat Kredit</li>
              </ul>
            </div>

            <div class="col-md-6">
              <ul>
                <li>Preprocessing</li>
                <li>Logistic Regression</li>
                <li>K-Nearest Neighbor</li>
              </ul>
            </div>
          </div>
        </div>

        <div class="col-lg-5">
          <div class="image-box"></div>
        </div>
      </div>
    </section>

    <!-- ================= RESULT ================= -->

    <section class="content-section container-fluid">
      <div class="row align-items-center g-4">
        <div class="col-lg-7">
          <h2 class="fw-bold">Hasil Prediksi</h2>

          <p class="text-muted mt-3">
            Setelah proses analisis selesai, sistem memberikan hasil berupa
            status kelayakan kredit, tingkat risiko, serta rekomendasi kredit.
          </p>

          <div class="row mt-4">
            <div class="col-md-4">
              <div class="result-card">
                <small>Skor</small>

                <h2>720</h2>
              </div>
            </div>

            <div class="col-md-4">
              <div class="result-card">
                <small>Risiko</small>

                <h2>Rendah</h2>
              </div>
            </div>

            <div class="col-md-4">
              <div class="result-card">
                <small>Kelayakan</small>

                <h2>Layak</h2>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-5">
          <div class="image-box"></div>
        </div>
      </div>
    </section>

    <!-- ================= FOOTER ================= -->

    <footer class="footer">
      <div class="container-fluid">
        <div class="row">
          <div class="col-md-4">
            <h5>Credit Risk Prediction</h5>

            <p>Sistem prediksi risiko kredit berbasis Machine Learning.</p>
          </div>

          <div class="col-md-4">
            <h6>Teknologi</h6>

            <ul>
              <li>Vue 3</li>
              <li>Flask</li>
              <li>Machine Learning</li>
            </ul>
          </div>

          <div class="col-md-4">
            <h6>Metode</h6>

            <ul>
              <li>Logistic Regression</li>
              <li>KNN</li>
            </ul>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

/*
|--------------------------------------------------------------------------
| ONBOARDING
|--------------------------------------------------------------------------
*/

const currentStep = ref(1);

const steps = [
  {
    title: "Input Data Nasabah",
    description:
      "Masukkan identitas dan informasi keuangan calon nasabah sebagai dasar analisis risiko kredit.",

    points: [
      "Nama, Nomor KTP, dan Pekerjaan",
      "Data Pendapatan dan Rasio Utang",
      "Riwayat Kredit Nasabah",
    ],
  },

  {
    title: "Analisis Machine Learning",
    description:
      "Data akan diproses menggunakan Logistic Regression untuk menentukan kelayakan kredit, kemudian K-Nearest Neighbor digunakan untuk menentukan tingkat risiko kredit.",

    points: [
      "Preprocessing Data",
      "Logistic Regression",
      "K-Nearest Neighbor (KNN)",
    ],
  },

  {
    title: "Hasil Prediksi",
    description:
      "Sistem menghasilkan status kelayakan kredit, probabilitas prediksi, tingkat risiko, dan rekomendasi plafon kredit sebagai pendukung keputusan.",

    points: [
      "Status Kelayakan Kredit",
      "Level Risiko Kredit",
      "Rekomendasi Kredit",
    ],
  },
];

const currentData = computed(() => {
  return steps[currentStep.value - 1];
});

/*
|--------------------------------------------------------------------------
| BUTTON
|--------------------------------------------------------------------------
*/

const nextStep = () => {
  if (currentStep.value < steps.length) {
    currentStep.value++;
  }
};

const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--;
  }
};

const goStep = (step) => {
  currentStep.value = step;
};

const goLogin = () => {
  router.push("/login");
};
</script>

<style scoped>
/* =======================================================
   GLOBAL
======================================================= */

.landing-page {
  background: #f4f6f9;
  min-height: 100vh;
}

/* =======================================================
   NAVBAR
======================================================= */

.navbar {
  height: 75px;
}

.navbar-brand {
  font-size: 24px;
  letter-spacing: 0.5px;
}

/* =======================================================
   HERO
======================================================= */

.hero-section {
  padding: 50px 70px;

  min-height: calc(100vh - 75px);

  display: flex;

  align-items: center;
}

.hero-card {
  background: #ececec;

  border-radius: 20px;

  padding: 40px;
}

.hero-card h1 {
  font-size: 60px;
}

.hero-card p {
  font-size: 18px;

  line-height: 1.8;
}

/* =======================================================
   IMAGE
======================================================= */

.image-box {
  background: white;

  border-radius: 20px;

  height: 430px;

  display: flex;

  align-items: center;

  justify-content: center;

  overflow: hidden;

  box-shadow: 0 5px 18px rgba(0, 0, 0, 0.08);
}

.image-box img {
  width: 100%;

  height: 100%;

  object-fit: cover;
}

/* =======================================================
   MINI CARD
======================================================= */

.mini-card {
  background: white;

  border-radius: 15px;

  padding: 22px;

  box-shadow: 0 5px 18px rgba(0, 0, 0, 0.08);

  transition: 0.3s;
}

.mini-card:hover {
  transform: translateY(-5px);
}

.mini-card h5 {
  font-weight: 700;
}

.mini-card p {
  font-size: 15px;

  line-height: 1.6;
}

/* =======================================================
   ONBOARDING
======================================================= */

.onboarding-card {
  background: #ececec;

  border-radius: 20px;

  padding: 35px;

  height: 100%;
}

.onboarding-card h2 {
  font-weight: 700;
}

.onboarding-card p {
  line-height: 1.8;
}

.onboarding-card ul {
  padding-left: 18px;
}

.onboarding-card li {
  margin-bottom: 12px;
}

/* =======================================================
   BUTTON STEP
======================================================= */

.step-btn {
  width: 42px;

  height: 42px;

  border-radius: 50%;

  border: none;

  background: #d5d5d5;

  margin: 5px;

  transition: 0.3s;

  font-weight: bold;
}

.step-btn:hover {
  transform: scale(1.08);
}

.step-btn.active {
  background: #0d6efd;

  color: white;
}

/* =======================================================
   CONTENT
======================================================= */

.content-section {
  padding: 80px 70px;
}

.content-section h2 {
  font-size: 40px;
}

.content-section p {
  font-size: 17px;

  line-height: 1.9;
}

.content-section ul {
  line-height: 2;
}

/* =======================================================
   RESULT CARD
======================================================= */

.result-card {
  background: white;

  border-radius: 18px;

  padding: 25px;

  text-align: center;

  box-shadow: 0 5px 18px rgba(0, 0, 0, 0.08);

  transition: 0.3s;
}

.result-card:hover {
  transform: translateY(-6px);
}

.result-card small {
  color: #666;
}

.result-card h2 {
  margin-top: 10px;

  font-weight: bold;

  color: #0d6efd;
}

/* =======================================================
   FOOTER
======================================================= */

.footer {
  margin-top: 70px;

  background: #1d1d1d;

  color: white;

  padding: 60px 70px;
}

.footer h5,
.footer h6 {
  margin-bottom: 20px;
}

.footer ul {
  list-style: none;

  padding: 0;
}

.footer li {
  margin-bottom: 10px;
}

.footer p {
  color: #d8d8d8;
}

/* =======================================================
   RESPONSIVE
======================================================= */

@media (max-width: 992px) {
  .hero-section {
    padding: 30px;
  }

  .content-section {
    padding: 30px;
  }

  .hero-card {
    margin-bottom: 30px;
  }

  .hero-card h1 {
    font-size: 42px;
  }

  .image-box {
    height: 280px;
  }
}
</style>
