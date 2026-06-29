<template>
  <div class="dashboard-page">
    <!-- HEADER -->

    <div class="top-header shadow-sm">
      <div class="logo-section">
        <h5 class="fw-bold mb-0">Risiko Kredit</h5>
      </div>

      <div class="search-section">
        <input
          v-model="search"
          class="form-control"
          placeholder="Cari nama atau NIK..."
        />
      </div>

      <router-link to="/prediction" class="btn btn-dark">
        + Prediksi Baru
      </router-link>

      <button
        class="btn btn-outline-danger logout-btn"
        @click="logout"
        title="Logout"
      >
        <i class="bi bi-box-arrow-right"></i>
      </button>

      <div class="user-info">
        <div class="text-end">
          <strong>
            {{ user?.nama_lengkap }}
          </strong>

          <br />

          <small>
            {{ user?.email }}
          </small>
        </div>
      </div>
    </div>

    <!-- BODY -->

    <div class="dashboard-layout">
      <!-- SIDEBAR -->

      <aside class="sidebar shadow-sm">
        <router-link to="/dashboard" class="menu-item active">
          🏠 Dashboard
        </router-link>

        <router-link to="/prediction" class="menu-item">
          ➕ Input Data
        </router-link>

        <router-link to="/history" class="menu-item"> 🕒 History </router-link>

        <router-link to="/profile" class="menu-item"> 👤 Profile </router-link>
      </aside>

      <!-- MAIN -->

      <main class="main-content">
        <!-- STAT CARD -->

        <div class="stats-grid">
          <div class="stat-card shadow-sm">
            <small>Total Prediksi</small>

            <h2>
              {{ totalPredictions }}
            </h2>
          </div>

          <div class="stat-card shadow-sm">
            <small>Layak</small>

            <h2 class="text-success">
              {{ totalLayak }}
            </h2>
          </div>

          <div class="stat-card shadow-sm">
            <small>Tidak Layak</small>

            <h2 class="text-danger">
              {{ totalTidakLayak }}
            </h2>
          </div>
        </div>

        <!-- CHART -->

        <div class="chart-grid">
          <div class="chart-card shadow-sm">
            <div class="chart-title">
              <span> Kredit Layak </span>

              <span> {{ persenLayak }}% </span>
            </div>

            <div style="height: 300px">
              <Pie :data="pieData" :options="pieOptions" />
            </div>
          </div>

          <div class="chart-card shadow-sm">
            <div class="chart-title">Distribusi Perkerjaan</div>

            <div style="height: 300px">
              <Bar :data="workData" :options="barOptions" />
            </div>
          </div>
        </div>

        <!-- TABLE -->

        <div class="table-card shadow-sm">
          <h5 class="mb-3">Prediksi Terakhir</h5>

          <div class="table-responsive">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th width="60">No</th>
                  <th>nama</th>
                  <th>Pekerjaan</th>
                  <th>Status</th>
                  <th>Risiko</th>
                  <th>Tanggal</th>
                </tr>
              </thead>

              <tbody>
                <tr
                  v-for="(item, index) in paginatedPredictions"
                  :key="item.id_prediction"
                >
                  <td>
                    {{ (currentPage - 1) * itemsPerPage + index + 1 }}
                  </td>

                  <td>
                    {{ item.name }}
                  </td>

                  <td>
                    {{ item.work }}
                  </td>

                  <td>
                    <span
                      class="badge"
                      :class="
                        item.result?.credit_eligibility === 'LAYAK'
                          ? 'bg-success'
                          : 'bg-danger'
                      "
                    >
                      {{ item.result?.credit_eligibility }}
                    </span>
                  </td>

                  <td>
                    <span
                      v-if="item.result?.risk_level"
                      class="badge"
                      :class="
                        item.result?.risk_level === 'RENDAH'
                          ? 'bg-success'
                          : 'bg-warning text-dark'
                      "
                    >
                      {{ item.result?.risk_level }}
                    </span>

                    <span v-else> - </span>
                  </td>

                  <td>
                    {{ formatDate(item.prediction_date) }}
                  </td>
                </tr>
              </tbody>
            </table>
            <div class="d-flex justify-content-between align-items-center mt-3">
              <button
                class="btn btn-outline-secondary"
                :disabled="currentPage === 1"
                @click="currentPage--"
              >
                ← Previous
              </button>

              <span> Halaman {{ currentPage }} dari {{ totalPages }} </span>

              <button
                class="btn btn-outline-secondary"
                :disabled="currentPage === totalPages"
                @click="currentPage++"
              >
                Next →
              </button>
            </div>
          </div>
        </div>
      </main>

      <!-- RIGHT PANEL -->

      <aside class="right-panel">
        <div class="side-card shadow-sm">
          <h6>Kesehatan Model</h6>

          <p>Uptime : 99.9%</p>

          <p>KNN : K=3</p>

          <p>Status : Aktif</p>
        </div>

        <div class="side-card shadow-sm">
          <h6>Tren Prediksi Harian</h6>

          <div style="height: 250px">
            <Line :data="lineData" :options="lineOptions" />
          </div>
        </div>

        <div class="side-card shadow-sm">
          <h6>Filter</h6>

          <button class="btn btn-sm btn-outline-secondary" @click="resetFilter">
            Reset
          </button>

          <div class="form-check">
            <input
              class="form-check-input"
              type="checkbox"
              v-model="filterLayak"
            />

            <label class="form-check-label"> Layak </label>
          </div>

          <div class="form-check">
            <input
              class="form-check-input"
              type="checkbox"
              v-model="filterTidakLayak"
            />

            <label class="form-check-label"> Tidak Layak </label>
          </div>

          <div class="form-check">
            <input
              class="form-check-input"
              type="checkbox"
              v-model="filterRendah"
            />

            <label class="form-check-label"> Risiko Rendah </label>
          </div>

          <div class="form-check">
            <input
              class="form-check-input"
              type="checkbox"
              v-model="filterTinggi"
            />

            <label class="form-check-label"> Risiko Tinggi </label>
          </div>
        </div>
      </aside>
    </div>

    <!-- FOOTER -->

    <footer class="footer">
      <div>
        <h6>Credit Risk</h6>

        <small> Sistem Prediksi Risiko Kredit </small>
      </div>

      <div>
        <h6>Produk</h6>

        <small>Dashboard</small><br />
        <small>Prediksi</small>
      </div>

      <div>
        <h6>Company</h6>

        <small>Tentang</small><br />
        <small>Karir</small>
      </div>

      <div>
        <h6>Support</h6>

        <small>Kontak</small><br />
        <small>Status</small>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import api from "../services/api";

import { watch } from "vue";

import { Pie, Bar, Line } from "vue-chartjs";

import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
} from "chart.js";

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
);

const router = useRouter();
const auth = useAuthStore();

const user = ref(null);
const predictions = ref([]);
const currentPage = ref(1);

const itemsPerPage = 5;

const search = ref("");

const filterLayak = ref(true);
const filterTidakLayak = ref(true);

const filterRendah = ref(true);
const filterTinggi = ref(true);

const getPredictions = async () => {
  try {
    const response = await api.get("/predictions");

    predictions.value = response.data.data || [];
  } catch (error) {
    console.error(error);
  }
};

const resetFilter = () => {
  search.value = "";

  filterLayak.value = true;
  filterTidakLayak.value = true;

  filterRendah.value = true;
  filterTinggi.value = true;
};

const filteredPredictions = computed(() => {
  return predictions.value.filter((item) => {
    const status = item.result?.credit_eligibility || "";
    const risk = item.result?.risk_level || "";

    const keyword = search.value.toLowerCase();

    const searchMatch =
      (item.name || "").toLowerCase().includes(keyword) ||
      (item.id_card || "").toLowerCase().includes(keyword) ||
      (item.work || "").toLowerCase().includes(keyword);

    const statusMatch =
      (!filterLayak.value && !filterTidakLayak.value) ||
      (filterLayak.value && status === "LAYAK") ||
      (filterTidakLayak.value && status === "TIDAK LAYAK");

    const riskMatch =
      (!filterRendah.value && !filterTinggi.value) ||
      (filterRendah.value && risk === "RENDAH") ||
      (filterTinggi.value && risk === "TINGGI");

    return searchMatch && statusMatch && riskMatch;
  });
});

const totalPages = computed(() =>
  Math.ceil(filteredPredictions.value.length / itemsPerPage),
);

const paginatedPredictions = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;

  return filteredPredictions.value.slice(start, start + itemsPerPage);
});

const totalPredictions = computed(() => filteredPredictions.value.length);

const totalLayak = computed(
  () =>
    filteredPredictions.value.filter(
      (p) => p.result?.credit_eligibility === "LAYAK",
    ).length,
);

const totalTidakLayak = computed(
  () =>
    filteredPredictions.value.filter(
      (p) => p.result?.credit_eligibility === "TIDAK LAYAK",
    ).length,
);

const persenLayak = computed(() => {
  if (!totalPredictions.value) return 0;

  return ((totalLayak.value / totalPredictions.value) * 100).toFixed(0);
});

const pieData = computed(() => ({
  labels: ["Layak", "Tidak Layak"],
  datasets: [
    {
      data: [totalLayak.value, totalTidakLayak.value],
      backgroundColor: ["#198754", "#dc3545"],
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

const workData = computed(() => {
  const pekerjaan = {};

  predictions.value.forEach((item) => {
    const work = item.work || "Tidak Diketahui";

    pekerjaan[work] = (pekerjaan[work] || 0) + 1;
  });

  return {
    labels: Object.keys(pekerjaan),

    datasets: [
      {
        label: "Jumlah Nasabah",

        data: Object.values(pekerjaan),

        backgroundColor: "#0d6efd",
      },
    ],
  };
});

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
        stepSize: 1,
        precision: 0,
      },
      title: {
        display: true,
        text: "Jumlah Nasabah",
      },
    },

    x: {
      title: {
        display: true,
        text: "Pekerjaan",
      },
    },
  },
};

watch(
  [search, filterLayak, filterTidakLayak, filterRendah, filterTinggi],
  () => {
    currentPage.value = 1;
  },
);

const lineData = computed(() => {
  const dataPerHari = {};

  predictions.value.forEach((item) => {
    const tanggal = new Date(item.prediction_date).toLocaleDateString("id-ID");

    dataPerHari[tanggal] = (dataPerHari[tanggal] || 0) + 1;
  });

  return {
    labels: Object.keys(dataPerHari),

    datasets: [
      {
        label: "Jumlah Prediksi",

        data: Object.values(dataPerHari),

        borderColor: "#0d6efd",

        backgroundColor: "#0d6efd",

        tension: 0.3,

        fill: false,
      },
    ],
  };
});

const lineOptions = {
  responsive: true,

  maintainAspectRatio: false,

  plugins: {
    legend: {
      display: true,
    },
  },

  scales: {
    y: {
      beginAtZero: true,

      ticks: {
        stepSize: 1,
      },

      title: {
        display: true,
        text: "Jumlah Prediksi",
      },
    },

    x: {
      title: {
        display: true,
        text: "Tanggal",
      },
    },
  },
};

const formatDate = (date) => {
  if (!date) return "-";

  return new Date(date).toLocaleString("id-ID");
};

onMounted(async () => {
  const storedUser = localStorage.getItem("user");

  if (storedUser) {
    user.value = JSON.parse(storedUser);
  }

  await getPredictions();
});

const logout = () => {
  auth.logout();

  router.push("/login");
};
</script>

<style scoped>
.dashboard-page {
  background: #f5f6fa;
  min-height: 100vh;
  padding: 20px;
}

.top-header {
  background: white;
  padding: 15px 20px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.logo-section {
  width: 180px;
}

.search-section {
  flex: 1;
}

.dashboard-layout {
  display: flex;
  gap: 20px;
}

.sidebar {
  width: 220px;
  background: white;
  border-radius: 12px;
  padding: 20px;
}

.menu-item {
  display: block;
  text-decoration: none;
  color: #333;
  padding: 12px;
  margin-bottom: 10px;
  border-radius: 10px;
}

.menu-item:hover {
  background: #eee;
}

.active {
  background: #ececec;
}

.main-content {
  flex: 1;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  margin-bottom: 15px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
}

.chart-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
  margin-bottom: 15px;
}

.chart-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
}

.chart-title {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}

.chart-placeholder {
  height: 240px;
  border: 2px dashed #ccc;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.table-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
}

.right-panel {
  width: 250px;
}

.side-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 15px;
}

.small-chart {
  height: 120px;
  border: 2px dashed #ccc;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 10px;
}

.footer {
  margin-top: 20px;
  background: white;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  justify-content: space-around;
}
</style>
