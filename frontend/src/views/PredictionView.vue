<template>
  <div class="container-fluid py-4">
    <!-- HEADER -->

    <div class="d-flex justify-content-between align-items-center mb-4">
      <div class="d-flex align-items-center">
        <button class="btn btn-light border me-3" @click="goBack">
          <i class="bi bi-arrow-left"></i>
        </button>

        <div>
          <h2 class="fw-bold mb-0">Prediksi Resiko Kredit</h2>

          <small class="text-muted">
            Sistem Prediksi Risiko Kredit menggunakan Logistic Regression dan
            KNN
          </small>
        </div>
      </div>

      <button class="btn btn-outline-secondary" @click="resetForm">
        <i class="bi bi-arrow-clockwise me-2"></i>
        Reset Form
      </button>
    </div>

    <div class="row g-4">
      <!-- ========================= -->
      <!-- INPUT -->
      <!-- ========================= -->

      <div class="col-lg-5">
        <div class="card shadow-sm border-0">
          <div class="card-body">
            <h5 class="fw-bold mb-4">
              <i class="bi bi-person-vcard me-2"></i>

              Data Nasabah
            </h5>

            <form @submit.prevent="predict">
              <!-- PERSONAL -->

              <!-- IDENTITAS NASABAH -->

              <div class="card shadow-sm mb-4">
                <div class="card-body">
                  <h4 class="mb-4">Identitas Nasabah</h4>

                  <div class="row">
                    <!-- Nama -->

                    <div class="col-md-6 mb-3">
                      <label class="form-label"> Nama Lengkap </label>

                      <input
                        v-model="form.name"
                        type="text"
                        class="form-control"
                        placeholder="Masukkan nama nasabah"
                        required
                      />
                    </div>

                    <!-- KTP -->

                    <div class="col-md-6 mb-3">
                      <label class="form-label"> Nomor KTP </label>

                      <input
                        v-model="form.id_card"
                        type="text"
                        maxlength="16"
                        class="form-control"
                        placeholder="16 digit nomor KTP"
                        required
                      />
                    </div>

                    <!-- Umur -->
                    <div class="col-md-6 mb-3">
                      <label class="form-label"> Umur </label>
                      <input
                        v-model.number="form.age"
                        type="number"
                        class="form-control"
                        required
                      />
                    </div>

                    <!-- Pekerjaan -->

                    <div class="col-md-6 mb-3">
                      <label class="form-label"> Pekerjaan </label>

                      <select v-model="form.work" class="form-select" required>
                        <option value="">-- Pilih Pekerjaan --</option>

                        <option
                          v-for="item in workOptions"
                          :key="item"
                          :value="item"
                        >
                          {{ item }}
                        </option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>

              <!-- FINANCIAL -->

              <div class="prediction-section mt-4">
                <h6>Data Keuangan</h6>

                <div class="mb-3">
                  <label class="form-label"> Pendapatan Bulanan (Rp) </label>

                  <input
                    v-model.number="form.monthly_income"
                    type="number"
                    class="form-control"
                    required
                  />
                </div>

                <div class="mb-3">
                  <label class="form-label"> Rasio Hutang </label>

                  <input
                    v-model.number="form.debt_ratio"
                    type="number"
                    step="0.01"
                    class="form-control"
                    required
                  />
                </div>

                <div class="mb-3">
                  <label class="form-label"> Jumlah Tanggungan </label>

                  <input
                    v-model.number="form.dependents"
                    type="number"
                    class="form-control"
                    required
                  />
                </div>

                <div>
                  <label class="form-label">
                    Persentase Penggunaan Kredit (%)
                  </label>

                  <input
                    v-model.number="form.revolving_utilization"
                    type="number"
                    step="0.01"
                    class="form-control"
                    required
                  />
                </div>
              </div>

              <!-- CREDIT -->

              <div class="prediction-section mt-4">
                <h6>Riwayat Kredit</h6>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label class="form-label"> Jumlah Fasilitas Kredit </label>

                    <input
                      v-model.number="form.number_credit"
                      type="number"
                      class="form-control"
                      required
                    />
                  </div>

                  <div class="col-md-6 mb-3">
                    <label class="form-label"> Jumlah Pinjaman Properti </label>

                    <input
                      v-model.number="form.real_estate_loans"
                      type="number"
                      class="form-control"
                      required
                    />
                  </div>

                  <div class="col-md-4 mb-3">
                    <label class="form-label"> Terlambat 30-59 Hari </label>

                    <input
                      v-model.number="form.delinquency_30_59"
                      type="number"
                      class="form-control"
                      required
                    />
                  </div>

                  <div class="col-md-4 mb-3">
                    <label class="form-label"> Terlambat 60-89 Hari </label>

                    <input
                      v-model.number="form.delinquency_60_89"
                      type="number"
                      class="form-control"
                      required
                    />
                  </div>

                  <div class="col-md-4 mb-3">
                    <label class="form-label"> Terlambat 90+ Hari </label>

                    <input
                      v-model.number="form.delinquency_90"
                      type="number"
                      class="form-control"
                      required
                    />
                  </div>
                </div>
              </div>

              <button
                class="btn btn-primary w-100 mt-4"
                type="submit"
                :disabled="loading"
              >
                <span
                  v-if="loading"
                  class="spinner-border spinner-border-sm me-2"
                ></span>

                {{ loading ? "Sedang memproses..." : "Mulai Prediksi" }}
              </button>
            </form>
          </div>
        </div>
      </div>

      <div class="col-lg-3">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <h5 class="fw-bold mb-4">
              <i class="bi bi-bar-chart-line me-2"></i>

              Hasil Prediksi
            </h5>

            <div v-if="!result" class="text-center py-5">
              <i
                class="bi bi-clipboard-data"
                style="font-size: 70px; color: #d1d5db"
              ></i>

              <p class="text-muted mt-3">Belum ada hasil prediksi.</p>
            </div>

            <div v-else>
              <!-- STATUS -->

              <div class="result-card text-center mb-4">
                <small class="text-muted"> Status Kredit </small>

                <h2
                  class="mt-2 fw-bold"
                  :class="
                    result.status === 'LAYAK' ? 'text-success' : 'text-danger'
                  "
                >
                  {{ result.status }}
                </h2>
              </div>

              <!-- PROBABILITY -->

              <div class="mb-4">
                <small class="text-muted"> Probabilitas Gagal Bayar </small>

                <h4 class="fw-bold">
                  {{ (result.probability * 100).toFixed(2) }}%
                </h4>

                <div class="progress mt-2">
                  <div
                    class="progress-bar"
                    :class="
                      result.status == 'LAYAK' ? 'bg-success' : 'bg-danger'
                    "
                    :style="{
                      width: result.probability * 100 + '%',
                    }"
                  ></div>
                </div>
              </div>

              <!-- RISK -->

              <div v-if="result.risk_level" class="mb-4">
                <small class="text-muted"> Tingkat Risiko </small>

                <div class="mt-2">
                  <span
                    class="badge px-3 py-2"
                    :class="
                      result.risk_level === 'RENDAH'
                        ? 'bg-success'
                        : 'bg-warning text-dark'
                    "
                  >
                    {{ result.risk_level }}
                  </span>
                </div>
              </div>

              <!-- PLAFOND -->

              <div class="mb-4">
                <small class="text-muted"> Plafond Rekomendasi </small>

                <h5 class="fw-bold mt-2">
                  {{ result.recommended_plafond || "-" }}
                </h5>
              </div>

              <!-- COLOR -->

              <div
                class="alert"
                :class="
                  result.status === 'LAYAK' ? 'alert-success' : 'alert-danger'
                "
              >
                <strong> Rekomendasi </strong>

                <hr />

                {{ result.recommendation }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ========================= -->
      <!-- INSIGHT -->
      <!-- ========================= -->

      <div class="col-lg-4">
        <div class="card shadow-sm border-0 h-100">
          <div class="card-body">
            <h5 class="fw-bold mb-4">
              <i class="bi bi-cpu me-2"></i>

              Analisis Sistem
            </h5>

            <div v-if="!result" class="text-center py-5">
              <i
                class="bi bi-lightbulb"
                style="font-size: 65px; color: #d1d5db"
              ></i>

              <p class="text-muted mt-3">
                Insight akan muncul setelah prediksi dilakukan.
              </p>
            </div>

            <div v-else>
              <div class="insight-box success-box mb-3">
                <h6>
                  <i class="bi bi-check-circle-fill me-2"></i>

                  Faktor positif
                </h6>

                <ul>
                  <li>Income mempengaruhi kemampuan pembayaran.</li>

                  <li>Age menunjukkan stabilitas finansial.</li>

                  <li>Revolving utilization rendah lebih baik.</li>
                </ul>
              </div>

              <div class="insight-box warning-box mb-3">
                <h6>
                  <i class="bi bi-exclamation-circle-fill me-2"></i>

                  Faktor risiko
                </h6>

                <ul>
                  <li>Debt Ratio tinggi meningkatkan risiko.</li>

                  <li>
                    Riwayat keterlambatan pembayaran menjadi faktor penting.
                  </li>
                </ul>
              </div>

              <div class="insight-box info-box">
                <h6>
                  <i class="bi bi-stars me-2"></i>

                  Rekomendasi Sistem
                </h6>

                <p class="mb-0">
                  {{ result.recommendation }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";

const router = useRouter();

const loading = ref(false);

const result = ref(null);

const form = reactive({
  name: "",
  id_card: "",
  work: "",
  revolving_utilization: 0,
  age: 0,
  delinquency_30_59: 0,
  debt_ratio: 0,
  monthly_income: 0,
  number_credit: 0,
  delinquency_90: 0,
  real_estate_loans: 0,
  delinquency_60_89: 0,
  dependents: 0,
});

const workOptions = [
  "Karyawan Swasta",
  "PNS",
  "Wirausaha",
  "Guru / Dosen",
  "Petani",
  "Nelayan",
  "Mahasiswa",
  "Ibu Rumah Tangga",
  "Freelancer",
  "Lainnya",
];

const predict = async () => {
  try {
    loading.value = true;

    const response = await api.post("/predict", form);

    result.value = response.data.result;
  } catch (error) {
    console.error(error);

    alert(
      error.response?.data?.message ||
        error.response?.data?.msg ||
        "Prediksi gagal",
    );
  } finally {
    loading.value = false;
  }
};

const resetForm = () => {
  form.revolving_utilization = 0;
  form.age = 0;
  form.delinquency_30_59 = 0;
  form.debt_ratio = 0;
  form.monthly_income = 0;
  form.number_credit = 0;
  form.delinquency_90 = 0;
  form.real_estate_loans = 0;
  form.delinquency_60_89 = 0;
  form.dependents = 0;

  result.value = null;
};

const goBack = () => {
  router.back();
};
</script>

<style scoped>
body {
  background: #f5f7fb;
}

.card {
  border: none;
  border-radius: 18px;
  transition: 0.3s;
}

.card:hover {
  transform: translateY(-2px);
}

.card-body {
  padding: 28px;
}

h2 {
  font-weight: 700;
}

h5 {
  font-weight: 600;
}

.prediction-section {
  border: 1px solid #e8ecf3;
  border-radius: 15px;
  padding: 20px;
  background: #fafbfc;
}

.prediction-section h6 {
  font-weight: 700;
  color: #0d6efd;
  margin-bottom: 18px;
}

.form-label {
  font-weight: 500;
  color: #495057;
}

.form-control {
  border-radius: 10px;
  min-height: 45px;
  border: 1px solid #dfe3e8;
}

.form-control:focus {
  box-shadow: 0 0 0 0.15rem rgba(13, 110, 253, 0.15);
  border-color: #0d6efd;
}

.btn {
  border-radius: 10px;
}

.btn-primary {
  height: 48px;
  font-weight: 600;
}

.result-card {
  border-radius: 15px;
  padding: 20px;
  background: #f8f9fa;
}

.progress {
  height: 10px;
  border-radius: 20px;
  overflow: hidden;
}

.progress-bar {
  transition: width 0.6s ease;
}

.badge {
  font-size: 0.95rem;
  border-radius: 10px;
}

.insight-box {
  border-radius: 14px;
  padding: 18px;
}

.insight-box h6 {
  font-weight: 700;
  margin-bottom: 12px;
}

.insight-box ul {
  padding-left: 18px;
  margin-bottom: 0;
}

.insight-box li {
  margin-bottom: 8px;
}

.success-box {
  background: #ecfdf3;
  border: 1px solid #b7ebc6;
}

.warning-box {
  background: #fff8e6;
  border: 1px solid #ffe39c;
}

.info-box {
  background: #eef4ff;
  border: 1px solid #bfd6ff;
}

.alert {
  border-radius: 12px;
}

.text-success {
  color: #198754 !important;
}

.text-danger {
  color: #dc3545 !important;
}

.spinner-border {
  width: 18px;
  height: 18px;
}

@media (max-width: 992px) {
  .prediction-section {
    margin-bottom: 20px;
  }

  .card {
    margin-bottom: 20px;
  }

  .card-body {
    padding: 20px;
  }
}

@media (max-width: 768px) {
  h2 {
    font-size: 1.5rem;
  }

  .card-body {
    padding: 16px;
  }

  .prediction-section {
    padding: 15px;
  }
}
</style>
