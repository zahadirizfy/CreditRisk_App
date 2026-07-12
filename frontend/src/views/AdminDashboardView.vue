<template>
  <div class="admin-dashboard">
    <!-- ===================================================== -->
    <!-- HEADER -->
    <!-- ===================================================== -->

    <header class="topbar">
      <div class="brand">
        <h2>Sistem Prediksi Resiko Kredit</h2>
        <small>Dashboard Administrator</small>
      </div>

      <div class="topbar-right">
        <div class="user-info">
          <div class="avatar">
            {{ user?.nama_lengkap?.charAt(0) || "A" }}
          </div>

          <div>
            <strong>{{ user?.nama_lengkap }}</strong>
            <br />
            <small>{{ user?.role }}</small>
          </div>
        </div>

        <button class="btn btn-outline-danger" @click="logout">Logout</button>
      </div>
    </header>

    <!-- ===================================================== -->
    <!-- BODY -->
    <!-- ===================================================== -->

    <div class="dashboard-body">
      <!-- ================= Sidebar ================= -->

      <aside class="sidebar">
        <h5>MENU</h5>

        <button class="menu-item active">🏠 Dashboard</button>

        <button class="menu-item" @click="showRetrainModal = true">
          🤖 Retrain Model
        </button>
      </aside>

      <!-- ================= Main ================= -->

      <main class="content">
        <!-- ===================================================== -->
        <!-- DASHBOARD STATISTIC -->
        <!-- ===================================================== -->

        <section class="statistics-section">
          <!-- TOTAL USER -->

          <div class="stat-card">
            <div class="stat-icon user-icon">👥</div>

            <div class="stat-body">
              <span class="stat-title"> Total Pengguna </span>

              <div v-if="loadingDashboard" class="placeholder-glow">
                <span class="placeholder col-4"></span>
              </div>

              <h2 v-else class="stat-value">
                {{ dashboard.total_user }}
              </h2>

              <small class="stat-subtitle"> Pengguna Terdaftar </small>
            </div>
          </div>

          <!-- TOTAL PREDIKSI -->

          <div class="stat-card">
            <div class="stat-icon prediction-icon">📄</div>

            <div class="stat-body">
              <span class="stat-title"> Total Prediksi </span>

              <div v-if="loadingDashboard" class="placeholder-glow">
                <span class="placeholder col-4"></span>
              </div>

              <h2 v-else class="stat-value">
                {{ dashboard.total_prediction }}
              </h2>

              <small class="stat-subtitle"> Prediksi yang Dilakukan </small>
            </div>
          </div>
        </section>

        <!-- PART 3 -->
        <section class="chart-section">
          <!-- Distribusi User -->

          <div class="chart-card">
            <div class="card-header-custom">
              <h5>👥 Distribusi Pengguna</h5>
            </div>

            <div class="chart-wrapper">
              <Pie :data="pieChartData" :options="pieOptions" />
            </div>
          </div>

          <!-- Aktivitas -->

          <div class="chart-card">
            <div class="card-header-custom">
              <h5>📈 Aktivitas Prediksi Bulanan</h5>
            </div>

            <div class="chart-wrapper">
              <Bar :data="predictionChartData" :options="barOptions" />
            </div>
          </div>
        </section>

        <!-- PART 4 -->
        <!-- ===================================================== -->
        <!-- KELOLA OPERATOR -->
        <!-- ===================================================== -->

        <section class="operator-card">
          <!-- HEADER -->

          <div class="operator-header">
            <div>
              <h4>👤 Kelola Operator</h4>

              <small> Daftar operator yang terdaftar pada sistem </small>
            </div>

            <button class="btn btn-primary" @click="showOperatorModal = true">
              + Tambah Operator
            </button>
          </div>

          <!-- TOOLBAR -->

          <div class="operator-toolbar">
            <input
              v-model="operatorSearch"
              @keyup.enter="loadOperator"
              type="text"
              class="operator-search"
              placeholder="🔍 Cari nama, username, email..."
            />
          </div>

          <!-- TABLE -->

          <div class="table-responsive">
            <table class="table operator-table">
              <thead>
                <tr>
                  <th>No</th>

                  <th>Nama</th>

                  <th>Username</th>

                  <th>Email</th>

                  <th>Instansi</th>

                  <th>Status</th>

                  <th>Aksi</th>
                </tr>
              </thead>

              <tbody>
                <tr v-if="loadingOperator">
                  <td colspan="7" class="text-center">
                    Memuat data operator...
                  </td>
                </tr>

                <tr v-else-if="operators.length === 0">
                  <td colspan="7" class="text-center">Belum ada operator.</td>
                </tr>

                <tr v-for="(item, index) in operators" :key="item.id_user">
                  <td>
                    {{ (operatorPage - 1) * 10 + index + 1 }}
                  </td>

                  <td>
                    {{ item.nama_lengkap }}
                  </td>

                  <td>
                    {{ item.username }}
                  </td>

                  <td>
                    {{ item.email }}
                  </td>

                  <td>
                    {{ item.instansi }}
                  </td>

                  <td>
                    <span
                      class="badge status-badge"
                      :class="item.status_aktif ? 'bg-success' : 'bg-danger'"
                      @click="changeStatus(item)"
                    >
                      {{ item.status_aktif ? "Aktif" : "Nonaktif" }}
                    </span>
                  </td>

                  <td>
                    <div class="d-flex gap-2">
                      <button
                        class="btn btn-sm btn-outline-primary"
                        @click="editOperator(item)"
                      >
                        ✏ Edit
                      </button>

                      <button
                        class="btn btn-sm btn-outline-danger"
                        @click="deleteOperator(item)"
                      >
                        🗑 Hapus
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
      </main>

      <!-- ================= Right Panel ================= -->

      <aside class="right-panel">
        <section class="panel-card">
          <h5 class="panel-title">🤖 Status Model</h5>

          <div class="mt-3">
            <small class="text-muted"> Model </small>

            <h6 class="fw-bold mt-1">
              {{ dashboard.model_status.model }}
            </h6>

            <span class="badge bg-success mt-2">
              {{ dashboard.model_status.status }}
            </span>

            <hr />

            <small class="text-muted"> Terakhir Dilatih </small>

            <p class="mb-0">
              {{ dashboard.model_status.last_retrain }}
            </p>
          </div>
        </section>

        <section class="panel-card">
          <h5 class="panel-title">📊 Evaluasi Model</h5>

          <div class="metric-row">
            <span>Accuracy</span>

            <strong>
              {{ (dashboard.evaluation.accuracy * 100).toFixed(2) }}%
            </strong>
          </div>

          <div class="metric-row">
            <span>Precision</span>

            <strong>
              {{ (dashboard.evaluation.precision * 100).toFixed(2) }}%
            </strong>
          </div>

          <div class="metric-row">
            <span>Recall</span>

            <strong>
              {{ (dashboard.evaluation.recall * 100).toFixed(2) }}%
            </strong>
          </div>

          <div class="metric-row">
            <span>F1 Score</span>

            <strong> {{ (dashboard.evaluation.f1 * 100).toFixed(2) }}% </strong>
          </div>

          <div class="metric-row">
            <span>ROC AUC</span>

            <strong>
              {{ (dashboard.evaluation.roc_auc * 100).toFixed(2) }}%
            </strong>
          </div>
        </section>

        <section class="panel-card">
          <h5 class="panel-title">📁 Dataset Training</h5>

          <p class="fw-bold mb-1">
            {{ dashboard.dataset.name }}
          </p>

          <small class="text-muted">
            Original :
            {{ dashboard.dataset.original }}
          </small>

          <br />

          <small class="text-muted">
            Training :
            {{ dashboard.dataset.training }}
          </small>

          <hr />

          <a
            :href="dashboard.dataset.url"
            target="_blank"
            class="btn btn-outline-primary btn-sm w-100"
          >
            🔗 Lihat Dataset Kaggle
          </a>
        </section>
      </aside>
    </div>

    <!-- ===================================================== -->
    <!-- FOOTER -->
    <!-- ===================================================== -->

    <footer class="dashboard-footer">
      <div class="footer-left">
        <h6>Sistem Prediksi Resiko Kredit</h6>

        <small> Hybrid Logistic Regression + KNN </small>
      </div>

      <div class="footer-center"></div>

      <div class="footer-right">
        <small> Version 1.0.0 </small>

        <small> © 2026 All Rights Reserved </small>
      </div>
    </footer>

    <!-- Modal Retrain -->
  </div>

  <!-- ===================================================== -->
  <!-- RETRAIN MODEL MODAL -->
  <!-- ===================================================== -->

  <div v-if="showRetrainModal" class="modal-overlay">
    <div class="operator-modal">
      <!-- HEADER -->

      <div class="modal-header-custom">
        <div>
          <h4>🤖 Retrain Machine Learning Model</h4>

          <small> Upload dataset baru untuk melakukan retraining model. </small>
        </div>

        <button class="close-btn" @click="showRetrainModal = false">✕</button>
      </div>

      <!-- BODY -->

      <div class="modal-body-custom">
        <!-- Upload -->

        <div class="upload-placeholder">
          <div class="upload-icon">📂</div>

          <h5>Upload Dataset (.CSV)</h5>

          <p class="mb-4">
            Dataset harus memiliki format yang sama dengan dataset training.
          </p>

          <input
            type="file"
            accept=".csv"
            class="form-control"
            @change="handleFile"
          />

          <!-- ========================= -->
          <!-- FILE TERPILIH -->
          <!-- ========================= -->

          <div v-if="selectedFile" class="selected-file mt-4">
            <strong>Dataset Dipilih</strong>
            <br />

            {{ selectedFile.name }}
          </div>

          <!-- ========================= -->
          <!-- PROGRESS RETRAIN -->

          <div v-if="loadingRetrain" class="mt-4">
            <div class="progress">
              <div
                class="progress-bar progress-bar-striped progress-bar-animated"
                :style="{ width: retrainProgress + '%' }"
              >
                {{ retrainProgress.toFixed(0) }}%
              </div>
            </div>

            <div class="mt-3">
              <strong> Step {{ retrainStep }} / {{ retrainTotalStep }} </strong>

              <br />

              {{ retrainStatus }}
            </div>
          </div>

          <!-- ========================= -->
          <!-- HASIL RETRAIN -->
          <!-- ========================= -->

          <div
            v-if="retrainMessage"
            class="alert mt-4"
            :class="retrainSuccess ? 'alert-success' : 'alert-danger'"
          >
            {{ retrainMessage }}
          </div>

          <div v-if="retrainResult && retrainSuccess" class="result-card mt-4">
            <h5 class="mb-3">📊 Hasil Retraining</h5>

            <table class="table table-sm">
              <tbody>
                <tr>
                  <td>Dataset</td>

                  <td>{{ retrainResult.dataset.filename }}</td>
                </tr>

                <tr>
                  <td>Jumlah Data</td>

                  <td>{{ retrainResult.dataset.rows }}</td>
                </tr>

                <tr>
                  <td>Accuracy</td>

                  <td>
                    {{
                      ((retrainResult.metrics?.accuracy || 0) * 100).toFixed(2)
                    }}%
                  </td>
                </tr>

                <tr>
                  <td>Precision</td>

                  <td>
                    {{
                      ((retrainResult.metrics?.precision || 0) * 100).toFixed(
                        2,
                      )
                    }}%
                  </td>
                </tr>

                <tr>
                  <td>Recall</td>

                  <td>
                    {{
                      ((retrainResult.metrics?.recall || 0) * 100).toFixed(2)
                    }}%
                  </td>
                </tr>

                <tr>
                  <td>F1 Score</td>

                  <td>
                    {{ ((retrainResult.metrics?.f1 || 0) * 100).toFixed(2) }}%
                  </td>
                </tr>

                <tr>
                  <td>ROC AUC</td>

                  <td>
                    {{
                      ((retrainResult.metrics?.roc_auc || 0) * 100).toFixed(2)
                    }}%
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- FOOTER -->

      <div class="modal-footer-custom">
        <button class="btn btn-secondary" @click="closeRetrainModal">
          Tutup
        </button>

        <button
          class="btn btn-primary"
          @click="retrainModel"
          :disabled="!selectedFile || loadingRetrain"
        >
          <span
            v-if="loadingRetrain"
            class="spinner-border spinner-border-sm me-2"
          ></span>

          {{ loadingRetrain ? "Processing..." : "Retrain Model" }}
        </button>
      </div>
    </div>
  </div>

  <!-- ===================================================== -->
  <!-- MODAL TAMBAH OPERATOR -->
  <!-- ===================================================== -->

  <div v-if="showOperatorModal" class="modal-overlay">
    <div class="operator-modal">
      <div class="modal-header-custom">
        <div>
          <h4>
            {{ isEditMode ? "✏ Edit Operator" : "👤 Tambah Operator" }}
          </h4>

          <small>
            {{
              isEditMode
                ? "Perbarui data operator."
                : "Tambahkan operator baru ke dalam sistem."
            }}
          </small>
        </div>

        <button class="close-btn" @click="closeOperatorModal">✕</button>
      </div>

      <div class="modal-body-custom">
        <div class="mb-3">
          <label>Nama Lengkap</label>

          <input v-model="operatorForm.nama_lengkap" class="form-control" />
        </div>

        <div class="mb-3">
          <label>Username</label>

          <input v-model="operatorForm.username" class="form-control" />
        </div>

        <div class="mb-3">
          <label>Email</label>

          <input
            v-model="operatorForm.email"
            type="email"
            class="form-control"
          />
        </div>

        <div class="mb-3">
          <label>No Telepon</label>

          <input v-model="operatorForm.nomor_telepon" class="form-control" />
        </div>

        <div class="mb-3">
          <label>Instansi</label>

          <input v-model="operatorForm.instansi" class="form-control" />
        </div>

        <div class="row">
          <div class="col">
            <label>Password</label>

            <input
              v-model="operatorForm.password"
              type="password"
              class="form-control"
            />
          </div>

          <div class="col">
            <label>Konfirmasi Password</label>

            <input
              v-model="operatorForm.confirm_password"
              type="password"
              class="form-control"
            />
          </div>
        </div>
      </div>

      <div class="modal-footer-custom">
        <button class="btn btn-secondary" @click="closeOperatorModal">
          Batal
        </button>

        <button
          class="btn btn-primary"
          @click="saveOperator"
          :disabled="loadingSaveOperator"
        >
          <span
            v-if="loadingSaveOperator"
            class="spinner-border spinner-border-sm me-2"
          ></span>

          {{
            loadingSaveOperator
              ? "Memproses..."
              : isEditMode
                ? "Update Operator"
                : "Simpan"
          }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "@/services/api";
import { computed } from "vue";
import Swal from "sweetalert2";

import {
  Chart as ChartJS,
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";

import { Pie, Bar } from "vue-chartjs";

ChartJS.register(
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
);

// =====================================================
// USER LOGIN
// =====================================================

const user = ref(JSON.parse(localStorage.getItem("user")) || {});

// =====================================================
// MODAL
// =====================================================

const showRetrainModal = ref(false);

// =====================================================
// MODAL OPERATOR
// =====================================================

const showOperatorModal = ref(false);

const operatorForm = ref({
  nama_lengkap: "",

  username: "",

  email: "",

  nomor_telepon: "",

  instansi: "",

  password: "",

  confirm_password: "",

  status_aktif: true,
});

// =====================================================
// SAVE OPERATOR
// =====================================================

const saveOperator = async () => {
  operatorError.value = "";

  operatorSuccess.value = "";

  // ===============================
  // VALIDASI
  // ===============================

  if (
    !operatorForm.value.nama_lengkap ||
    !operatorForm.value.username ||
    !operatorForm.value.email
  ) {
    operatorError.value = "Semua field wajib diisi.";

    return;
  }

  if (!isEditMode.value && !operatorForm.value.password) {
    operatorError.value = "Password wajib diisi.";

    return;
  }

  if (
    operatorForm.value.password &&
    operatorForm.value.password !== operatorForm.value.confirm_password
  ) {
    operatorError.value = "Konfirmasi password tidak sama.";

    return;
  }

  loadingSaveOperator.value = true;

  try {
    const payload = {
      nama_lengkap: operatorForm.value.nama_lengkap,

      username: operatorForm.value.username,

      email: operatorForm.value.email,

      nomor_telepon: operatorForm.value.nomor_telepon,

      instansi: operatorForm.value.instansi,

      password: operatorForm.value.password,
    };

    let res;

    if (isEditMode.value) {
      res = await api.put(
        `/operators/${selectedOperatorId.value}`,

        payload,
      );
    } else {
      res = await api.post(
        "/operators",

        payload,
      );
    }

    await loadOperator();

    closeOperatorModal();

    await Swal.fire({
      icon: "success",

      title: "Berhasil",

      text: res.data.message,

      confirmButtonColor: "#0d6efd",

      confirmButtonText: "OK",
    });
  } catch (err) {
    await Swal.fire({
      icon: "error",

      title: "Gagal",

      text: err.response?.data?.message || "Terjadi kesalahan.",

      confirmButtonColor: "#dc3545",
    });
  } finally {
    loadingSaveOperator.value = false;
  }
};

// =====================================================
// DASHBOARD DATA
// =====================================================

const dashboard = ref({
  total_user: 0,
  total_prediction: 0,
  user_distribution: {},
  monthly_prediction: [],

  model_status: {
    model: "",
    status: "",
    last_retrain: "-",
  },

  dataset: {
    name: "",
    original: 0,
    training: 0,
    url: "",
  },

  evaluation: {
    accuracy: 0,
    precision: 0,
    recall: 0,
    f1: 0,
    roc_auc: 0,
  },
});

// =====================================================
// PIE CHART
// =====================================================

const roleColor = {
  super_admin: "#ef4444",
  operator: "#3b82f6",
  nasabah: "#22c55e",
  instansi: "#f59e0b",
};

const pieChartData = computed(() => ({
  labels: Object.keys(dashboard.value.user_distribution),

  datasets: [
    {
      data: Object.values(dashboard.value.user_distribution),

      backgroundColor: Object.keys(dashboard.value.user_distribution).map(
        (role) => roleColor[role] || "#94a3b8",
      ),

      borderColor: "#ffffff",

      borderWidth: 2,

      hoverOffset: 10,
    },
  ],
}));

// =====================================================
// BAR CHART
// =====================================================

const predictionChartData = computed(() => ({
  labels: dashboard.value.monthly_prediction.map((i) => i.month),

  datasets: [
    {
      label: "Jumlah Prediksi",

      data: dashboard.value.monthly_prediction.map((i) => i.total),

      backgroundColor: "#2563eb",

      borderRadius: 10,

      maxBarThickness: 45,
    },
  ],
}));

const pieOptions = {
  responsive: true,

  maintainAspectRatio: false,

  plugins: {
    legend: {
      position: "bottom",

      labels: {
        usePointStyle: true,

        pointStyle: "circle",

        padding: 20,

        font: {
          size: 13,
        },
      },
    },
  },
};

const barOptions = {
  responsive: true,

  maintainAspectRatio: false,

  plugins: {
    legend: {
      display: false,
    },
  },

  scales: {
    y: {
      beginAtZero: true,

      ticks: {
        precision: 0,
      },

      grid: {
        color: "#edf2f7",
      },
    },

    x: {
      grid: {
        display: false,
      },
    },
  },
};

// =====================================================
// CHART
// =====================================================

const userChart = ref(null);

const predictionChart = ref(null);

// =====================================================
// OPERATOR
// =====================================================

const operators = ref([]);

const operatorPagination = ref({});

const operatorSearch = ref("");

const operatorPage = ref(1);

// =====================================================
// PAGINATION
// =====================================================

const currentPage = ref(1);

const perPage = ref(10);

// =====================================================
// LOADING
// =====================================================

const loadingDashboard = ref(false);

const loadingOperator = ref(false);

// =====================================================
// LOAD DASHBOARD
// =====================================================

const loadDashboard = async () => {
  loadingDashboard.value = true;

  try {
    const res = await api.get("/dashboard");

    if (res.data.success) {
      dashboard.value = res.data.data;

      console.log("Dashboard Loaded", dashboard.value);
    }
  } catch (err) {
    console.error("Dashboard Error :", err);
  } finally {
    loadingDashboard.value = false;
  }
};

// =====================================================
// LOAD OPERATOR
// (Part 4)
// =====================================================

// =====================================================
// LOAD OPERATOR
// =====================================================

const loadOperator = async () => {
  loadingOperator.value = true;

  try {
    const res = await api.get("/operators", {
      params: {
        page: operatorPage.value,

        per_page: 10,

        search: operatorSearch.value,
      },
    });

    operators.value = res.data.data.operators;

    operatorPagination.value = res.data.data.pagination;
  } catch (err) {
    console.error(err);
  } finally {
    loadingOperator.value = false;
  }
};

// =====================================================
// SEARCH OPERATOR
// (Part 4)
// =====================================================

//const searchData = () => {
// const keyword = operatorSearch.value.toLowerCase();
// };

const operatorError = ref("");

const operatorSuccess = ref("");

const loadingSaveOperator = ref(false);

const resetOperatorForm = () => {
  operatorForm.value = {
    nama_lengkap: "",

    username: "",

    email: "",

    nomor_telepon: "",

    instansi: "",

    password: "",

    confirm_password: "",

    status_aktif: true,
  };

  operatorError.value = "";

  operatorSuccess.value = "";

  isEditMode.value = false;

  selectedOperatorId.value = null;
};

const closeOperatorModal = () => {
  resetOperatorForm();

  showOperatorModal.value = false;
};

// =====================================================
// EDIT OPERATOR
// =====================================================

const editOperator = (item) => {
  isEditMode.value = true;

  selectedOperatorId.value = item.id_user;

  operatorForm.value = {
    nama_lengkap: item.nama_lengkap,

    username: item.username,

    email: item.email,

    nomor_telepon: item.nomor_telepon,

    instansi: item.instansi,

    password: "",

    confirm_password: "",

    status_aktif: item.status_aktif,
  };

  showOperatorModal.value = true;
};

const changeStatus = async (item) => {
  const result = await Swal.fire({
    title: item.status_aktif ? "Nonaktifkan Operator?" : "Aktifkan Operator?",

    html: item.status_aktif
      ? `
        <b>${item.nama_lengkap}</b>
        <br><br>
        Operator tidak akan dapat login ke sistem.
      `
      : `
        <b>${item.nama_lengkap}</b>
        <br><br>
        Operator dapat kembali menggunakan sistem.
      `,

    icon: "question",

    showCancelButton: true,

    confirmButtonText: item.status_aktif ? "Ya, Nonaktifkan" : "Ya, Aktifkan",

    cancelButtonText: "Batal",

    confirmButtonColor: item.status_aktif ? "#dc3545" : "#198754",

    cancelButtonColor: "#6c757d",
  });

  if (!result.isConfirmed) return;

  try {
    const res = await api.patch(
      `/operators/${item.id_user}/status`,

      {
        status_aktif: !item.status_aktif,
      },
    );

    await loadOperator();

    await Swal.fire({
      icon: "success",

      title: "Berhasil",

      text: res.data.message,

      confirmButtonColor: "#0d6efd",
    });
  } catch (err) {
    await Swal.fire({
      icon: "error",

      title: "Gagal",

      text: err.response?.data?.message || "Gagal mengubah status operator.",

      confirmButtonColor: "#dc3545",
    });
  }
};

// =====================================================
// DELETE OPERATOR
// =====================================================

const deleteOperator = async (item) => {
  const result = await Swal.fire({
    title: "Hapus Operator",

    html: `
      <div style="text-align:center">

        <p>Apakah Anda yakin ingin menghapus operator berikut?</p>

        <h5 style="margin:15px 0;color:#0d6efd">
          ${item.nama_lengkap}
        </h5>

        <small style="color:#6c757d">
          Data operator yang dihapus tidak dapat dikembalikan.
        </small>

      </div>
    `,

    icon: "warning",

    showCancelButton: true,

    confirmButtonColor: "#dc3545",

    cancelButtonColor: "#6c757d",

    confirmButtonText: "Ya, Hapus",

    cancelButtonText: "Batal",
  });

  if (!result.isConfirmed) return;

  try {
    const res = await api.delete(`/operators/${item.id_user}`);

    await loadOperator();

    await Swal.fire({
      icon: "success",

      title: "Berhasil",

      text: res.data.message,

      confirmButtonColor: "#0d6efd",
    });
  } catch (err) {
    await Swal.fire({
      icon: "error",

      title: "Gagal",

      text: err.response?.data?.message || "Operator gagal dihapus.",

      confirmButtonColor: "#dc3545",
    });
  }
};

// =====================================================
// LOGOUT
// =====================================================

const logout = async () => {
  const result = await Swal.fire({
    title: "Logout",

    text: "Apakah Anda yakin ingin keluar dari sistem?",

    icon: "question",

    showCancelButton: true,

    confirmButtonColor: "#dc3545",

    cancelButtonColor: "#6c757d",

    confirmButtonText: "Ya, Logout",

    cancelButtonText: "Batal",
  });

  if (!result.isConfirmed) return;

  localStorage.removeItem("token");

  localStorage.removeItem("user");

  window.location.href = "/";
};

// =====================================================
// HANDLE FILE
// =====================================================

const handleFile = (event) => {
  const file = event.target.files[0];

  if (!file) return;

  if (!file.name.toLowerCase().endsWith(".csv")) {
    alert("File harus berformat CSV.");

    event.target.value = "";

    return;
  }

  selectedFile.value = file;

  retrainMessage.value = "";
};

// =====================================================
// RESET MODAL
// =====================================================

const closeRetrainModal = () => {
  showRetrainModal.value = false;

  selectedFile.value = null;

  retrainMessage.value = "";

  retrainSuccess.value = false;

  loadingRetrain.value = false;

  retrainResult.value = null;
};

// =====================================================
// LIFECYCLE
// =====================================================

onMounted(async () => {
  await loadDashboard();

  // Part 4
  await loadOperator();

  // Part 3
  // renderUserChart();

  // renderPredictionChart();
});

// =====================================================
// EDIT MODE
// =====================================================

const isEditMode = ref(false);

const selectedOperatorId = ref(null);

// =====================================================
// RETRAIN
// =====================================================

const selectedFile = ref(null);

const retrainMessage = ref("");

const retrainSuccess = ref(false);

const loadingRetrain = ref(false);

const retrainResult = ref(null);

const retrainProgress = ref(0);

const retrainStep = ref(0);

const retrainTotalStep = ref(6);

const retrainStatus = ref("");

let progressInterval = null;

const startPollingStatus = () => {
  progressInterval = setInterval(async () => {
    try {
      const res = await api.get("/retrain-status");

      const data = res.data.data;

      retrainStep.value = data.step;

      retrainTotalStep.value = data.total_step;

      retrainStatus.value = data.message;

      retrainProgress.value = (data.step / data.total_step) * 100;

      if (data.status === "success" || data.status === "failed") {
        clearInterval(progressInterval);
      }
    } catch (err) {
      console.error(err);
    }
  }, 1000);
};

const retrainModel = async () => {
  if (!selectedFile.value) return;

  loadingRetrain.value = true;

  retrainProgress.value = 0;

  retrainStep.value = 0;

  retrainStatus.value = "";

  retrainMessage.value = "";

  const formData = new FormData();

  formData.append("dataset", selectedFile.value);

  startPollingStatus();

  try {
    const res = await api.post("/retrain", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    retrainSuccess.value = res.data.success;

    retrainMessage.value = res.data.message;

    retrainResult.value = res.data;

    await loadDashboard();
  } catch (err) {
    retrainSuccess.value = false;

    retrainMessage.value = err.response?.data?.message || "Retraining gagal.";
  } finally {
    loadingRetrain.value = false;
  }
};
</script>

<style scoped src="../css/AdminDashboardView.css"></style>
