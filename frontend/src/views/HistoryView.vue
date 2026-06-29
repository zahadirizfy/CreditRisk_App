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

            <p class="mb-1">
              Layak :
              <strong>{{ totalLayak }}</strong>
            </p>

            <p class="mb-0">
              Tidak Layak :
              <strong>{{ totalTidakLayak }}</strong>
            </p>
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

              <router-link to="/prediction" class="btn btn-dark">
                + Prediksi Baru
              </router-link>
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
                      {{ index + 1 }}
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
                      <button
                        class="btn btn-sm btn-primary"
                        @click="viewDetail(item)"
                      >
                        Detail
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import api from "../services/api";
import { useRouter } from "vue-router";

const predictions = ref([]);
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
</script>
