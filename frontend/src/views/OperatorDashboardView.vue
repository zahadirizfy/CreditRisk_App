<template>
  <div class="operator-dashboard">
    <!-- ===================================================== -->
    <!-- HEADER -->
    <!-- ===================================================== -->

    <header class="topbar">
      <div class="brand">
        <h2>Sistem Prediksi Resiko Kredit</h2>
        <small>Dashboard Operator</small>
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
      </aside>

      <!-- ================= Main ================= -->

      <main class="content">
        <!-- ===================================================== -->
        <!-- STATISTIC -->
        <!-- ===================================================== -->

        <section class="statistics-section">
          <!-- Total User -->

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

          <!-- Total Prediksi -->

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

        <!-- ===================================================== -->
        <!-- CHART -->
        <!-- ===================================================== -->

        <section class="chart-section">
          <!-- Pie -->

          <div class="chart-card">
            <div class="card-header-custom">
              <h5>👥 Distribusi Pengguna</h5>
            </div>

            <div class="chart-wrapper">
              <Pie :data="pieChartData" :options="pieOptions" />
            </div>
          </div>

          <!-- Bar -->

          <div class="chart-card">
            <div class="card-header-custom">
              <h5>📈 Aktivitas Prediksi Bulanan</h5>
            </div>

            <div class="chart-wrapper">
              <Bar :data="predictionChartData" :options="barOptions" />
            </div>
          </div>
        </section>

        <!-- ===================================================== -->
        <!-- KELOLA NASABAH -->
        <!-- ===================================================== -->

        <section class="operator-card">
          <div class="operator-header">
            <div>
              <h4>👥 Kelola Nasabah / Instansi</h4>

              <small>
                Daftar nasabah dan instansi yang terdaftar pada sistem
              </small>
            </div>

            <button class="btn btn-primary" @click="showCustomerModal = true">
              + Tambah
            </button>
          </div>

          <div class="operator-toolbar">
            <input
              v-model="customerSearch"
              @keyup.enter="searchCustomer"
              class="operator-search"
              placeholder="🔍 Cari nama, username atau instansi..."
            />
          </div>

          <div class="table-responsive">
            <table class="table operator-table">
              <thead>
                <tr>
                  <th>No</th>

                  <th>Nama</th>

                  <th>Username</th>

                  <th>Role</th>

                  <th>Instansi</th>

                  <th>Status</th>

                  <th>Aksi</th>
                </tr>
              </thead>

              <tbody>
                <tr v-if="loadingCustomer">
                  <td colspan="7" class="text-center">Memuat data...</td>
                </tr>

                <tr v-else-if="customers.length === 0">
                  <td colspan="7" class="text-center">
                    Belum ada data nasabah.
                  </td>
                </tr>

                <tr v-for="(item, index) in customers" :key="item.id_user">
                  <td>
                    {{ (customerPage - 1) * 10 + index + 1 }}
                  </td>

                  <td>
                    {{ item.nama_lengkap }}
                  </td>

                  <td>
                    {{ item.username }}
                  </td>

                  <td>
                    <span
                      class="badge"
                      :class="
                        item.role === 'nasabah' ? 'bg-success' : 'bg-primary'
                      "
                    >
                      {{ item.role === "nasabah" ? "Nasabah" : "Instansi" }}
                    </span>
                  </td>

                  <td>
                    {{ item.instansi || "-" }}
                  </td>

                  <td>
                    <span
                      class="badge status-badge"
                      :class="item.status_aktif ? 'bg-success' : 'bg-danger'"
                      @click="changeCustomerStatus(item)"
                    >
                      {{ item.status_aktif ? "Aktif" : "Nonaktif" }}
                    </span>
                  </td>

                  <td>
                    <div class="d-flex gap-2">
                      <button
                        class="btn btn-sm btn-outline-primary"
                        @click="editCustomer(item)"
                      >
                        Edit
                      </button>

                      <button
                        class="btn btn-sm btn-outline-danger"
                        @click="deleteCustomer(item)"
                      >
                        Hapus
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
            <div v-if="customerPagination.pages > 1" class="pagination-wrapper">
              <button
                class="btn btn-outline-secondary"
                :disabled="customerPage === 1"
                @click="changePage(customerPage - 1)"
              >
                ← Sebelumnya
              </button>

              <span class="pagination-info">
                Halaman
                <strong>{{ customerPagination.page }}</strong>
                dari
                <strong>{{ customerPagination.pages }}</strong>
              </span>

              <button
                class="btn btn-outline-secondary"
                :disabled="customerPage === customerPagination.pages"
                @click="changePage(customerPage + 1)"
              >
                Selanjutnya →
              </button>
            </div>
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
              {{ dashboard.model_status.model || "-" }}
            </h6>

            <span class="badge bg-success mt-2">
              {{ dashboard.model_status.status || "-" }}
            </span>

            <hr />

            <small class="text-muted"> Terakhir Dilatih </small>

            <p class="mb-0">
              {{ dashboard.model_status.last_retrain || "-" }}
            </p>
          </div>
        </section>

        <section class="panel-card">
          <h5 class="panel-title">📊 Evaluasi Model</h5>

          <div class="metric-row">
            <span>Accuracy</span>
            <strong
              >{{
                ((dashboard.evaluation.accuracy || 0) * 100).toFixed(2)
              }}%</strong
            >
          </div>

          <div class="metric-row">
            <span>Precision</span>
            <strong>
              {{
                ((dashboard.evaluation.precision || 0) * 100).toFixed(2)
              }}%</strong
            >
          </div>

          <div class="metric-row">
            <span>Recall</span>
            <strong
              >{{
                ((dashboard.evaluation.recall || 0) * 100).toFixed(2)
              }}%</strong
            >
          </div>

          <div class="metric-row">
            <span>F1 Score</span>
            <strong>
              {{ ((dashboard.evaluation.f1 || 0) * 100).toFixed(2) }}%</strong
            >
          </div>

          <div class="metric-row">
            <span>ROC AUC</span>
            <strong>
              {{
                ((dashboard.evaluation.roc_auc || 0) * 100).toFixed(2)
              }}%</strong
            >
          </div>
        </section>

        <section class="panel-card">
          <h5 class="panel-title">📁 Dataset Training</h5>

          <p class="fw-bold mb-1">
            {{ dashboard.dataset.name || "-" }}
          </p>

          <small class="text-muted">
            Original :
            {{ dashboard.dataset.original || "-" }}
          </small>

          <br />

          <small class="text-muted">
            Training :
            {{ dashboard.dataset.training || "-" }}
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

        <small>Hybrid Logistic Regression + KNN</small>
      </div>

      <div class="footer-right">
        <small>Version 1.0.0</small>

        <small>© 2026 All Rights Reserved</small>
      </div>
    </footer>
  </div>

  <!-- ===================================================== -->
  <!-- MODAL TAMBAH NASABAH / INSTANSI -->
  <!-- ===================================================== -->

  <div v-if="showCustomerModal" class="modal-overlay">
    <div class="operator-modal">
      <!-- HEADER -->

      <div class="modal-header-custom">
        <div>
          <h4>
            {{
              editMode
                ? "✏️ Edit Nasabah / Instansi"
                : "👥 Tambah Nasabah / Instansi"
            }}
          </h4>

          <small> Tambahkan data pengguna baru. </small>
        </div>

        <button class="close-btn" @click="closeCustomerModal">✕</button>
      </div>

      <!-- BODY -->

      <div class="modal-body-custom">
        <div class="mb-3">
          <label>Nama Lengkap</label>

          <input v-model="customerForm.nama_lengkap" class="form-control" />
        </div>

        <div class="mb-3">
          <label>Username</label>

          <input v-model="customerForm.username" class="form-control" />
        </div>

        <div class="mb-3">
          <label>Email</label>

          <input
            v-model="customerForm.email"
            type="email"
            class="form-control"
          />
        </div>

        <div class="mb-3">
          <label>No. Telepon</label>

          <input v-model="customerForm.nomor_telepon" class="form-control" />
        </div>

        <div class="mb-3">
          <label>Role</label>

          <select v-model="customerForm.role" class="form-select">
            <option value="nasabah">Nasabah</option>

            <option value="instansi">Instansi</option>
          </select>
        </div>

        <div v-if="customerForm.role == 'instansi'" class="mb-3">
          <label>Nama Instansi</label>

          <input v-model="customerForm.instansi" class="form-control" />
        </div>

        <div v-if="!editMode" class="row">
          <div class="col">
            <label>Password</label>

            <input
              v-model="customerForm.password"
              type="password"
              class="form-control"
            />
          </div>

          <div class="col">
            <label>Konfirmasi Password</label>

            <input
              v-model="customerForm.confirm_password"
              type="password"
              class="form-control"
            />
          </div>
        </div>

        <div v-if="customerError" class="alert alert-danger mt-3">
          {{ customerError }}
        </div>

        <div v-if="customerSuccess" class="alert alert-success mt-3">
          {{ customerSuccess }}
        </div>
      </div>

      <!-- FOOTER -->

      <div class="modal-footer-custom">
        <button class="btn btn-secondary" @click="closeCustomerModal">
          Batal
        </button>

        <button
          class="btn btn-primary"
          @click="saveCustomer"
          :disabled="loadingSaveCustomer"
        >
          <span
            v-if="loadingSaveCustomer"
            class="spinner-border spinner-border-sm me-2"
          ></span>

          {{
            loadingSaveCustomer
              ? editMode
                ? "Mengupdate..."
                : "Menyimpan..."
              : editMode
                ? "Update"
                : "Simpan"
          }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { Pie, Bar } from "vue-chartjs";
import api from "@/services/api";
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
// DASHBOARD
// =====================================================

const dashboard = ref({
  total_user: 0,

  total_prediction: 0,

  user_distribution: {},

  monthly_prediction: [],

  model_status: {},

  dataset: {},

  evaluation: {},
});
// =====================================================
// CUSTOMER
// =====================================================

const customers = ref([]);

const customerPagination = ref({});

const customerSearch = ref("");

const customerPage = ref(1);

const loadingCustomer = ref(false);

// =====================================================
// MODAL CUSTOMER
// =====================================================

const showCustomerModal = ref(false);

// =====================================================
// EDIT MODE
// =====================================================

const editMode = ref(false);

const selectedCustomerId = ref(null);

const loadingSaveCustomer = ref(false);

const customerError = ref("");

const customerSuccess = ref("");

const customerForm = ref({
  nama_lengkap: "",

  username: "",

  email: "",

  nomor_telepon: "",

  instansi: "",

  role: "nasabah",

  password: "",

  confirm_password: "",
});

const resetCustomerForm = () => {
  editMode.value = false;

  selectedCustomerId.value = null;

  customerForm.value = {
    nama_lengkap: "",

    username: "",

    email: "",

    nomor_telepon: "",

    instansi: "",

    role: "nasabah",

    password: "",

    confirm_password: "",
  };

  customerError.value = "";

  customerSuccess.value = "";
};

const closeCustomerModal = () => {
  resetCustomerForm();

  showCustomerModal.value = false;
};

const saveCustomer = async () => {
  customerError.value = "";
  customerSuccess.value = "";

  if (
    !customerForm.value.nama_lengkap ||
    !customerForm.value.username ||
    !customerForm.value.email
  ) {
    customerError.value = "Semua field wajib diisi.";
    return;
  }

  // Password hanya wajib saat tambah
  if (!editMode.value) {
    if (!customerForm.value.password) {
      customerError.value = "Password wajib diisi.";
      return;
    }

    if (customerForm.value.password !== customerForm.value.confirm_password) {
      customerError.value = "Konfirmasi password tidak sama.";
      return;
    }
  }

  loadingSaveCustomer.value = true;

  try {
    const payload = {
      nama_lengkap: customerForm.value.nama_lengkap,
      username: customerForm.value.username,
      email: customerForm.value.email,
      nomor_telepon: customerForm.value.nomor_telepon,
      instansi: customerForm.value.instansi,
      role: customerForm.value.role,
    };

    // Password hanya dikirim saat tambah
    if (!editMode.value) {
      payload.password = customerForm.value.password;
    }

    let res;

    if (editMode.value) {
      res = await api.put(`/customers/${selectedCustomerId.value}`, payload);
    } else {
      res = await api.post("/customers", {
        ...payload,
        password: customerForm.value.password,
      });
    }

    customerSuccess.value = res.data.message;

    await loadCustomer();

    setTimeout(() => {
      closeCustomerModal();
    }, 800);
  } catch (err) {
    customerError.value = err.response?.data?.message || "Terjadi kesalahan.";
  } finally {
    loadingSaveCustomer.value = false;
  }
};

const changeCustomerStatus = async (item) => {
  const action = item.status_aktif ? "menonaktifkan" : "mengaktifkan";

  const result = await Swal.fire({
    title: `${item.status_aktif ? "Nonaktifkan" : "Aktifkan"} Akun?`,

    text: `Yakin ingin ${action} ${item.nama_lengkap}?`,

    icon: "question",

    showCancelButton: true,

    confirmButtonText: "Ya",

    cancelButtonText: "Batal",
  });

  if (!result.isConfirmed) return;

  try {
    await api.patch(`/customers/${item.id_user}/status`, {
      status_aktif: !item.status_aktif,
    });

    await loadCustomer();

    Swal.fire({
      icon: "success",

      title: "Berhasil",

      timer: 1200,

      showConfirmButton: false,
    });
  } catch (err) {
    Swal.fire({
      icon: "error",

      title: "Gagal",

      text: err.response?.data?.message || "Terjadi kesalahan",
    });
  }
};
const editCustomer = (item) => {
  editMode.value = true;

  selectedCustomerId.value = item.id_user;

  customerForm.value = {
    nama_lengkap: item.nama_lengkap,

    username: item.username,

    email: item.email,

    nomor_telepon: item.nomor_telepon,

    instansi: item.instansi,

    role: item.role,

    password: "",

    confirm_password: "",
  };

  customerError.value = "";

  customerSuccess.value = "";

  showCustomerModal.value = true;
};

// =====================================================
// DELETE CUSTOMER
// =====================================================

const deleteCustomer = async (item) => {
  const result = await Swal.fire({
    title: "Hapus Data",

    text: `Yakin ingin menghapus ${item.nama_lengkap}?`,

    icon: "warning",

    showCancelButton: true,

    confirmButtonColor: "#dc3545",

    cancelButtonColor: "#6c757d",

    confirmButtonText: "Ya, Hapus",

    cancelButtonText: "Batal",
  });

  if (!result.isConfirmed) return;

  try {
    const res = await api.delete(`/customers/${item.id_user}`);

    await Swal.fire({
      icon: "success",

      title: "Berhasil",

      text: res.data.message,

      timer: 1500,

      showConfirmButton: false,
    });

    await loadCustomer();
  } catch (err) {
    Swal.fire({
      icon: "error",

      title: "Gagal",

      text: err.response?.data?.message || "Terjadi kesalahan.",
    });
  }
};

// =====================================================
// LOADING
// =====================================================

const loadingDashboard = ref(false);

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

      borderWidth: 2,

      borderColor: "#fff",
    },
  ],
}));

// =====================================================
// BAR CHART
// =====================================================

const predictionChartData = computed(() => ({
  labels: dashboard.value.monthly_prediction.map((item) => item.month),

  datasets: [
    {
      label: "Jumlah Prediksi",

      data: dashboard.value.monthly_prediction.map((item) => item.total),

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
};

// =====================================================
// LOAD DASHBOARD
// =====================================================

const loadDashboard = async () => {
  loadingDashboard.value = true;

  try {
    const res = await api.get("/customers/dashboard");

    if (res.data.success) {
      dashboard.value = res.data.data;

      console.log("Dashboard Loaded");
      console.log(dashboard.value);
    }
  } catch (err) {
    console.error(err);
  } finally {
    loadingDashboard.value = false;
  }
};

// =====================================================
// LOGOUT
// =====================================================

const logout = async () => {
  const result = await Swal.fire({
    title: "Logout",

    text: "Apakah Anda yakin ingin keluar?",

    icon: "question",

    showCancelButton: true,

    confirmButtonColor: "#dc3545",

    cancelButtonColor: "#6c757d",

    confirmButtonText: "Logout",

    cancelButtonText: "Batal",
  });

  if (!result.isConfirmed) return;

  localStorage.removeItem("token");

  localStorage.removeItem("user");

  window.location.href = "/login";
};

// =====================================================
// LOAD CUSTOMER
// =====================================================

const loadCustomer = async () => {
  loadingCustomer.value = true;

  try {
    const res = await api.get("/customers", {
      params: {
        page: customerPage.value,

        per_page: 10,

        search: customerSearch.value,
      },
    });

    customers.value = res.data.data.customers;

    customerPagination.value = res.data.data.pagination;
  } catch (err) {
    console.error(err);
  } finally {
    loadingCustomer.value = false;
  }
};

// =====================================================
// PAGINATION
// =====================================================

const changePage = async (page) => {
  if (page < 1 || page > customerPagination.value.pages) {
    return;
  }

  customerPage.value = page;

  await loadCustomer();
};

// =====================================================
// LIFECYCLE
// =====================================================

onMounted(async () => {
  await loadDashboard();

  await loadCustomer();
});

const searchCustomer = async () => {
  customerPage.value = 1;

  await loadCustomer();
};
</script>

<style scoped src="../css/OperatorDashboardView.css"></style>
