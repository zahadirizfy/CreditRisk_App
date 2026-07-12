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
                  <img :src="currentData.image" class="hero-image" />
                </div>
              </div>

              <!-- INFO -->

              <div class="col-md-5">
                <div class="mini-card">
                  <small class="text-muted">
                    Langkah {{ currentStep }} dari 3
                  </small>

                  <h5 class="mt-2">
                    {{ currentData.title2 }}
                  </h5>

                  <p>
                    {{ currentData.description2 }}
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
            Sistem ini memanfaatkan data historis dan informasi keuangan calon
            nasabah sebagai dasar dalam proses analisis risiko kredit. Data yang
            dimasukkan akan melalui tahap preprocessing untuk meningkatkan
            kualitas data sebelum diproses oleh model Machine Learning. Model
            Logistic Regression digunakan untuk memprediksi kelayakan pemberian
            kredit berdasarkan karakteristik nasabah, sedangkan metode K-Nearest
            Neighbor (KNN) digunakan untuk mengelompokkan tingkat risiko kredit
            berdasarkan kemiripan pola dengan data historis. Kombinasi kedua
            metode tersebut menghasilkan proses analisis yang lebih objektif,
            cepat, dan konsisten sehingga dapat membantu lembaga keuangan dalam
            mendukung pengambilan keputusan kredit.
          </p>

          <div class="row mt-4">
            <div class="col-md-6">
              <h5>Data Nasabah</h5>
              <ul>
                <li>Identitas Nasabah</li>
                <li>Data Keuangan</li>
                <li>Riwayat Kredit</li>
                <li>Rasio Hutang</li>
                <li>Jumlah Tanggungan</li>
              </ul>
            </div>

            <div class="col-md-6">
              <h5>Proses Machine Learning</h5>
              <ul>
                <li>Data Preprocessing</li>
                <li>Feature Engineering</li>
                <li>Logistic Regression</li>
                <li>K-Nearest Neighbor</li>
                <li>Hasil Prediksi</li>
              </ul>
            </div>
          </div>
        </div>

        <div class="col-lg-5">
          <div class="image-box">
            <img :src="mlImage" alt="Machine Learning" class="content-image" />
          </div>
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
                <small>Probabilitas</small>

                <h2><0.7</h2>
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
          <div class="image-box">
            <img
              :src="resultImage"
              alt="Machine Learning"
              class="content-image"
            />
          </div>
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
import step1 from "@/assets/step1.png";
import step2 from "@/assets/step2.png";
import step3 from "@/assets/step3.png";
import mlImage from "@/assets/mlimage.png";
import resultImage from "@/assets/resultimage.png";

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
    title2: "Mulai dari Data yang Akurat",

    image: step1,

    description:
      "Masukkan identitas dan informasi keuangan calon nasabah sebagai dasar analisis risiko kredit.",
    description2:
      "Kualitas hasil prediksi sangat bergantung pada data yang dimasukkan. Pastikan seluruh informasi nasabah diisi dengan benar dan lengkap agar sistem dapat menghasilkan analisis risiko yang lebih akurat.",

    points: [
      "Nama, Nomor KTP, dan Pekerjaan",
      "Data Pendapatan dan Rasio Utang",
      "Riwayat Kredit Nasabah",
    ],
  },

  {
    title: "Analisis Machine Learning",
    title2: "Analisis Dilakukan Secara Otomatis",
    image: step2,
    description:
      "Data akan diproses menggunakan Logistic Regression untuk menentukan kelayakan kredit, kemudian K-Nearest Neighbor digunakan untuk menentukan tingkat risiko kredit.",
    description2:
      "Setelah data dikirim, sistem akan melakukan preprocessing kemudian menganalisis data menggunakan Logistic Regression dan K-Nearest Neighbor (KNN). Seluruh proses berlangsung secara otomatis hanya dalam beberapa detik.",

    points: [
      "Preprocessing Data",
      "Logistic Regression",
      "K-Nearest Neighbor (KNN)",
    ],
  },

  {
    title: "Hasil Prediksi",
    title2: "Informasi Siap Digunakan",
    image: step3,
    description:
      "Sistem menghasilkan status kelayakan kredit, probabilitas prediksi, tingkat risiko, dan rekomendasi plafon kredit sebagai pendukung keputusan.",
    description2:
      "Hasil prediksi menampilkan status kelayakan kredit, tingkat risiko, probabilitas, serta rekomendasi plafon kredit yang dapat digunakan sebagai bahan pertimbangan dalam proses pengambilan keputusan.",

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

<style scoped src="../css/LandingView.css"></style>
