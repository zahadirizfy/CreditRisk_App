<template>
  <div class="container-fluid mt-4">
    <div class="row">
      <!-- SIDEBAR -->

      <div class="col-lg-3 mb-4">
        <div class="card shadow-sm mb-3">
          <div class="card-body">
            <div class="d-flex justify-content-between mb-3">
              <h5>Filter</h5>

              <button
                class="btn btn-sm btn-outline-secondary"
                @click="resetFilter"
              >
                Reset
              </button>
            </div>

            <!-- STATUS -->

            <h6>Status Kelayakan</h6>

            <div class="form-check">
              <input
                class="form-check-input"
                type="checkbox"
                v-model="filterLayak"
              />

              <label class="form-check-label"> Layak </label>
            </div>

            <div class="form-check mb-3">
              <input
                class="form-check-input"
                type="checkbox"
                v-model="filterTidakLayak"
              />

              <label class="form-check-label"> Tidak Layak </label>
            </div>

            <!-- RISK -->

            <h6>Level Risiko</h6>

            <div class="form-check">
              <input
                class="form-check-input"
                type="checkbox"
                v-model="filterRendah"
              />

              <label class="form-check-label"> Rendah </label>
            </div>

            <div class="form-check">
              <input
                class="form-check-input"
                type="checkbox"
                v-model="filterTinggi"
              />

              <label class="form-check-label"> Tinggi </label>
            </div>
          </div>
        </div>

        <!-- SUMMARY -->

        <div class="card shadow-sm mb-3">
          <div class="card-body">
            <h6>Ringkasan</h6>

            <div class="text-start mb-3">
              <div class="summary-number text-success">
                {{ totalLayak }}
              </div>

              <small>Layak</small>
            </div>

            <div class="text-start">
              <div class="summary-number text-danger">
                {{ totalTidakLayak }}
              </div>

              <small>Tidak Layak</small>
            </div>
          </div>
        </div>
      </div>

      <!-- CONTENT -->

      <div class="col-lg-9">
        <div class="card shadow-sm">
          <div class="card-body">
            <!-- HEADER -->

            <div class="d-flex justify-content-between align-items-center mb-4">
              <div>
                <div class="d-flex align-items-center gap-2 mb-2">
                  <button
                    class="btn btn-outline-secondary btn-sm"
                    @click="goBack"
                  >
                    ← Back
                  </button>
                </div>

                <h2 class="mb-0">Riwayat Prediksi</h2>

                <small class="text-muted">
                  Riwayat seluruh prediksi kredit
                </small>
              </div>

              <div class="d-flex gap-2">
                <button class="btn btn-success" @click="exportExcel">
                  📥 Export Excel
                </button>

                <button class="btn btn-danger" @click="exportPDF">
                  📄 Export PDF
                </button>

                <router-link to="/prediction" class="btn btn-dark">
                  + Prediksi Baru
                </router-link>
              </div>
            </div>

            <!-- SEARCH -->

            <div class="row mb-3">
              <div class="col-md-6">
                <input
                  v-model="search"
                  type="text"
                  class="form-control"
                  placeholder="Cari berdasarkan nama atau pekerjaan..."
                />
              </div>
            </div>

            <!-- TABLE -->

            <div class="table-responsive">
              <table class="table table-bordered align-middle">
                <thead class="table-dark">
                  <tr>
                    <th>No</th>
                    <th>Nama</th>
                    <th>Pekerjaan</th>
                    <th>Kelayakan</th>
                    <th>Risiko</th>
                    <th>Probabilitas</th>
                    <th>Tanggal</th>
                    <th>Aksi</th>
                  </tr>
                </thead>

                <tbody>
                  <tr
                    v-for="(item, index) in filteredPredictions"
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
                          item.result.risk_level === 'RENDAH'
                            ? 'bg-success'
                            : 'bg-warning text-dark'
                        "
                      >
                        {{ item.result.risk_level }}
                      </span>

                      <span v-else>-</span>
                    </td>

                    <td>
                      {{
                        item.result
                          ? formatProbability(item.result.logistic_probability)
                          : "-"
                      }}
                    </td>

                    <td>
                      {{ formatDate(item.prediction_date) }}
                    </td>

                    <td>
                      <div class="d-flex gap-2">
                        <button
                          class="btn btn-primary btn-sm"
                          @click="openDetail(item)"
                        >
                          Detail
                        </button>

                        <button
                          class="btn btn-danger btn-sm"
                          @click="openDelete(item)"
                        >
                          Hapus
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
              <div
                class="d-flex justify-content-between align-items-center mt-4"
              >
                <small class="text-muted">
                  Menampilkan

                  {{ paginatedPredictions.length }}

                  dari

                  {{ filteredPredictions.length }}

                  data
                </small>

                <nav>
                  <ul class="pagination mb-0">
                    <li
                      class="page-item"
                      :class="{ disabled: currentPage === 1 }"
                    >
                      <button class="page-link" @click="currentPage--">
                        Previous
                      </button>
                    </li>

                    <li
                      v-for="page in totalPages"
                      :key="page"
                      class="page-item"
                      :class="{ active: currentPage === page }"
                    >
                      <button class="page-link" @click="currentPage = page">
                        {{ page }}
                      </button>
                    </li>

                    <li
                      class="page-item"
                      :class="{ disabled: currentPage === totalPages }"
                    >
                      <button class="page-link" @click="currentPage++">
                        Next
                      </button>
                    </li>
                  </ul>
                </nav>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- ================================================= -->
  <!-- DETAIL MODAL -->
  <!-- ================================================= -->

  <div v-if="showDetailModal" class="modal-overlay" @click.self="closeDetail">
    <div class="detail-modal">
      <!-- HEADER -->

      <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h3 class="fw-bold mb-1">Detail Prediksi</h3>

          <small class="text-muted">
            Informasi lengkap hasil prediksi kredit
          </small>
        </div>

        <button class="btn-close" @click="closeDetail"></button>
      </div>

      <div v-if="selectedPrediction">
        <!-- ================================================= -->
        <!-- RINGKASAN -->
        <!-- ================================================= -->

        <div class="row g-3 mb-4">
          <div class="col-md-4">
            <div class="summary-card">
              <small>Status Kelayakan</small>

              <div
                class="badge fs-6 mt-2"
                :class="
                  selectedPrediction.result.credit_eligibility === 'LAYAK'
                    ? 'bg-success'
                    : 'bg-danger'
                "
              >
                {{ selectedPrediction.result.credit_eligibility }}
              </div>
            </div>
          </div>

          <div class="col-md-4">
            <div class="summary-card">
              <small>Tingkat Risiko</small>

              <div
                class="badge fs-6 mt-2"
                :class="
                  selectedPrediction.result.risk_level === 'RENDAH'
                    ? 'bg-success'
                    : 'bg-warning text-dark'
                "
              >
                {{ selectedPrediction.result.risk_level || "-" }}
              </div>
            </div>
          </div>

          <div class="col-md-4">
            <div class="summary-card">
              <small>Probabilitas</small>

              <h4 class="mt-2">
                {{
                  formatProbability(
                    selectedPrediction.result.logistic_probability,
                  )
                }}
              </h4>
            </div>
          </div>
        </div>

        <!-- ================================================= -->
        <!-- IDENTITAS -->
        <!-- ================================================= -->

        <div class="info-card">
          <div class="info-title">👤 Identitas Nasabah</div>

          <div class="row mt-3">
            <div class="col-md-4">
              <small>Nama</small>

              <h6>{{ selectedPrediction.name }}</h6>
            </div>

            <div class="col-md-4">
              <small>No. KTP</small>

              <h6>{{ selectedPrediction.id_card }}</h6>
            </div>

            <div class="col-md-4">
              <small>Pekerjaan</small>

              <h6>{{ selectedPrediction.work }}</h6>
            </div>
          </div>
        </div>

        <!-- ================================================= -->
        <!-- DATA KEUANGAN -->
        <!-- ================================================= -->

        <div class="info-card">
          <div class="info-title">💰 Data Keuangan</div>

          <div class="row mt-3">
            <div class="col-md-4">
              <small>Usia</small>

              <h6>{{ selectedPrediction.age }} Tahun</h6>
            </div>

            <div class="col-md-4">
              <small>Pendapatan</small>

              <h6>
                Rp
                {{
                  Number(selectedPrediction.monthly_income).toLocaleString(
                    "id-ID",
                  )
                }}
              </h6>
            </div>

            <div class="col-md-4">
              <small>Debt Ratio</small>

              <h6>{{ selectedPrediction.debt_ratio }}</h6>
            </div>

            <div class="col-md-4 mt-3">
              <small>Revolving Utilization</small>

              <h6>{{ selectedPrediction.revolving_utilization }}</h6>
            </div>

            <div class="col-md-4 mt-3">
              <small>Jumlah Kredit</small>

              <h6>{{ selectedPrediction.number_credit }}</h6>
            </div>

            <div class="col-md-4 mt-3">
              <small>Jumlah Tanggungan</small>

              <h6>{{ selectedPrediction.dependents }}</h6>
            </div>
          </div>
        </div>

        <!-- ================================================= -->
        <!-- RIWAYAT KREDIT -->
        <!-- ================================================= -->

        <div class="info-card">
          <div class="info-title">📋 Riwayat Kredit</div>

          <div class="row mt-3">
            <div class="col-md-4">
              <small>Terlambat 30-59 Hari</small>

              <h6>{{ selectedPrediction.delinquency_30_59 }}</h6>
            </div>

            <div class="col-md-4">
              <small>Terlambat 60-89 Hari</small>

              <h6>{{ selectedPrediction.delinquency_60_89 }}</h6>
            </div>

            <div class="col-md-4">
              <small>Terlambat >90 Hari</small>

              <h6>{{ selectedPrediction.delinquency_90 }}</h6>
            </div>
          </div>
        </div>

        <!-- FOOTER -->

        <div class="text-end">
          <button class="btn btn-secondary" @click="closeDetail">Tutup</button>
        </div>
      </div>
    </div>
  </div>

  <!-- ========================================= -->
  <!-- DELETE MODAL -->
  <!-- ========================================= -->

  <div v-if="showDeleteModal" class="modal-overlay" @click.self="closeDelete">
    <div class="bg-white p-4 rounded-4" style="width: 420px">
      <div class="text-center">
        <div class="mb-3" style="font-size: 55px">🗑️</div>

        <h4>Hapus Prediksi?</h4>

        <p class="text-muted">
          Data prediksi atas nama

          <strong>
            {{ selectedDelete?.name }}
          </strong>

          akan dihapus secara permanen.
        </p>
      </div>

      <div class="d-flex justify-content-end gap-2 mt-4">
        <button class="btn btn-secondary" @click="closeDelete">Batal</button>

        <button
          class="btn btn-danger"
          @click="deletePrediction"
          :disabled="deleting"
        >
          {{ deleting ? "Menghapus..." : "Ya, Hapus" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import api from "../services/api";
import { useRouter } from "vue-router";
import Swal from "sweetalert2";
import * as XLSX from "xlsx";
import { saveAs } from "file-saver";
import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

const predictions = ref([]);
const showDetailModal = ref(false);

const selectedPrediction = ref(null);
const showDeleteModal = ref(false);

const selectedDelete = ref(null);

const deleting = ref(false);
const openDelete = (prediction) => {
  selectedDelete.value = prediction;

  showDeleteModal.value = true;
};

const closeDelete = () => {
  showDeleteModal.value = false;

  selectedDelete.value = null;
};
const deletePrediction = async () => {
  try {
    deleting.value = true;

    await api.delete(`/predictions/${selectedDelete.value.id_prediction}`);

    closeDelete();

    await getPredictions();

    Swal.fire({
      icon: "success",
      title: "Berhasil",
      text: "Prediksi berhasil dihapus.",
      confirmButtonText: "OK",
      confirmButtonColor: "#0d6efd",
    });
  } catch (error) {
    Swal.fire({
      icon: "error",
      title: "Gagal",
      text: error.response?.data?.message || "Gagal menghapus data.",
    });
  } finally {
    deleting.value = false;
  }
};
const loading = ref(false);

const search = ref("");

const filterLayak = ref(false);
const filterTidakLayak = ref(false);

const filterRendah = ref(false);
const filterTinggi = ref(false);

const getPredictions = async () => {
  try {
    loading.value = true;

    const response = await api.get("/predictions");

    predictions.value = response.data.data || [];
  } catch (error) {
    alert(error.response?.data?.message || "Gagal mengambil data");
  } finally {
    loading.value = false;
  }
};

const totalLayak = computed(
  () =>
    predictions.value.filter((p) => p.result?.credit_eligibility === "LAYAK")
      .length,
);

const totalTidakLayak = computed(
  () =>
    predictions.value.filter(
      (p) => p.result?.credit_eligibility === "TIDAK LAYAK",
    ).length,
);

const filteredPredictions = computed(() => {
  return predictions.value.filter((item) => {
    const status = item.result?.credit_eligibility;

    const risk = item.result?.risk_level;

    const keyword = search.value.toLowerCase();

    const searchMatch =
      item.name?.toLowerCase().includes(keyword) ||
      item.work?.toLowerCase().includes(keyword) ||
      status?.toLowerCase().includes(keyword);

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

const resetFilter = () => {
  search.value = "";

  filterLayak.value = false;
  filterTidakLayak.value = false;

  filterRendah.value = false;
  filterTinggi.value = false;
};

const openDetail = (prediction) => {
  selectedPrediction.value = prediction;

  showDetailModal.value = true;
};

const closeDetail = () => {
  showDetailModal.value = false;

  selectedPrediction.value = null;
};

const formatDate = (date) => new Date(date).toLocaleString("id-ID");

const formatProbability = (value) => {
  const percent = value * 100;

  if (percent < 0.0001) {
    return "< 0.0001%";
  }

  return percent.toFixed(4) + "%";
};

onMounted(() => {
  getPredictions();
});

const router = useRouter();

const goBack = () => {
  router.back();
};
const exportExcel = () => {
  const data = filteredPredictions.value.map((item, index) => ({
    No: index + 1,
    Nama: item.name,
    "No. KTP": item.id_card,
    Pekerjaan: item.work,
    Usia: item.age,
    Pendapatan: item.monthly_income,
    "Debt Ratio": item.debt_ratio,
    "Jumlah Kredit": item.number_credit,
    "Jumlah Tanggungan": item.dependents,
    Status: item.result?.credit_eligibility,
    Risiko: item.result?.risk_level,
    Probabilitas: formatProbability(item.result?.logistic_probability),
    "Tanggal Prediksi": formatDate(item.prediction_date),
  }));

  const worksheet = XLSX.utils.json_to_sheet(data);

  const workbook = XLSX.utils.book_new();

  XLSX.utils.book_append_sheet(workbook, worksheet, "Riwayat Prediksi");

  const excelBuffer = XLSX.write(workbook, {
    bookType: "xlsx",
    type: "array",
  });

  const file = new Blob([excelBuffer], {
    type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
  });

  saveAs(
    file,
    `Riwayat_Prediksi_${new Date().toLocaleDateString("id-ID")}.xlsx`,
  );
};

const exportPDF = () => {
  const doc = new jsPDF();

  // =============================
  // JUDUL
  // =============================

  doc.setFontSize(18);

  doc.text("Laporan Riwayat Prediksi Kredit", 14, 18);

  doc.setFontSize(11);

  doc.text(`Tanggal Export : ${new Date().toLocaleString("id-ID")}`, 14, 26);

  // =============================
  // DATA
  // =============================

  const rows = filteredPredictions.value.map((item, index) => [
    index + 1,

    item.name,

    item.work,

    item.result?.credit_eligibility,

    item.result?.risk_level || "-",

    formatProbability(item.result?.logistic_probability),

    formatDate(item.prediction_date),
  ]);

  autoTable(doc, {
    startY: 35,

    head: [
      [
        "No",
        "Nama",
        "Pekerjaan",
        "Status",
        "Risiko",
        "Probabilitas",
        "Tanggal",
      ],
    ],

    body: rows,

    styles: {
      fontSize: 9,

      cellPadding: 3,

      valign: "middle",
    },

    headStyles: {
      fillColor: [37, 99, 235],

      textColor: 255,

      halign: "center",
    },

    alternateRowStyles: {
      fillColor: [245, 245, 245],
    },
  });

  doc.save("Riwayat_Prediksi.pdf");
};

const currentPage = ref(1);

const itemsPerPage = 10;
const totalPages = computed(() => {
  return Math.ceil(filteredPredictions.value.length / itemsPerPage);
});
const paginatedPredictions = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;

  const end = start + itemsPerPage;

  return filteredPredictions.value.slice(start, end);
});
</script>


<style scoped src="../css/HistoryView.css"></style>