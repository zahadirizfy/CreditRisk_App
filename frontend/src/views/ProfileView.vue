<template>
  <div class="container-fluid mt-4">
    <div class="mb-3">
      <button class="btn btn-outline-secondary" @click="goBack">← Back</button>
    </div>

    <div
      v-if="notification.show"
      class="alert mb-3"
      :class="'alert-' + notification.type"
    >
      {{ notification.message }}
    </div>
    <div v-if="loading" class="text-center">Memuat data...</div>

    <div v-else-if="user" class="row">
      <!-- SIDEBAR -->

      <div class="col-lg-4 mb-4">
        <div class="card shadow-sm profile-card">
          <div class="card-body text-center">
            <div class="avatar-box mx-auto mb-3">
              {{ user.nama_lengkap?.charAt(0).toUpperCase() }}
            </div>

            <h4>
              {{ user.nama_lengkap }}
            </h4>

            <p class="text-muted">
              {{ user.email }}
            </p>

            <div class="row mt-4">
              <div class="col-6">
                <h5>Role</h5>
                <p>{{ user.role }}</p>
              </div>

              <div class="col-6">
                <h5>Status</h5>

                <span
                  class="badge"
                  :class="user.status_aktif ? 'bg-success' : 'bg-danger'"
                >
                  {{ user.status_aktif ? "Aktif" : "Tidak Aktif" }}
                </span>
              </div>
            </div>

            <hr />

            <div class="text-start">
              <p>
                <strong>Telepon :</strong>
                <br />
                {{ user.nomor_telepon || "-" }}
              </p>

              <p>
                <strong>Institusi :</strong>
                <br />
                {{ user.institusi || "-" }}
              </p>

              <p>
                <strong>Username :</strong>
                <br />
                {{ user.username }}
              </p>
            </div>

            <button
              class="btn btn-outline-primary w-100 mt-2"
              @click="toggleEdit"
            >
              {{ editMode ? "Cancel" : "Edit Profile" }}
            </button>
          </div>
        </div>
      </div>

      <!-- CONTENT -->

      <div class="col-lg-8">
        <!-- PERSONAL INFO -->

        <div class="card shadow-sm mb-4">
          <div class="card-body">
            <h4 class="mb-4">Informasi Pribadi</h4>

            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label"> Nama Lengkap </label>

                <input
                  type="text"
                  class="form-control"
                  v-model="profileForm.nama_lengkap"
                  :readonly="!editMode"
                />
              </div>

              <div class="col-md-6 mb-3">
                <label class="form-label"> Nomor Telepon </label>

                <input
                  type="text"
                  class="form-control"
                  v-model="profileForm.nomor_telepon"
                  :readonly="!editMode"
                />
              </div>

              <div class="col-md-6 mb-3">
                <label class="form-label"> Username </label>

                <input
                  type="text"
                  class="form-control"
                  v-model="profileForm.username"
                  :readonly="!editMode"
                />
              </div>

              <div class="col-md-6 mb-3">
                <label class="form-label"> Email </label>

                <input
                  type="text"
                  class="form-control"
                  v-model="profileForm.email"
                  :readonly="!editMode"
                />
              </div>

              <div v-if="user.role !== 'nasabah'" class="col-md-6 mb-3">
                <label class="form-label"> Institusi </label>

                <input
                  type="text"
                  class="form-control"
                  v-model="profileForm.institusi"
                  :readonly="!editMode"
                />
              </div>
            </div>
          </div>
        </div>

        <div class="text-end" v-if="editMode">
          <button
            class="btn btn-primary"
            @click="saveProfile"
            :disabled="savingProfile"
          >
            {{ savingProfile ? "Saving..." : "Save Changes" }}
          </button>
        </div>

        <!-- SECURITY -->

        <div class="card shadow-sm">
          <div class="card-body">
            <h4 class="mb-4">Keamanan</h4>

            <div class="row">
              <div class="col-md-4 mb-3">
                <label class="form-label"> Password Lama </label>

                <input
                  type="password"
                  class="form-control"
                  v-model="passwordForm.current_password"
                  placeholder="********"
                />
              </div>

              <div class="col-md-4 mb-3">
                <label class="form-label"> Password Baru </label>

                <input
                  type="password"
                  class="form-control"
                  v-model="passwordForm.new_password"
                  placeholder="********"
                />
              </div>

              <div class="col-md-4 mb-3">
                <label class="form-label"> Konfirmasi Password </label>

                <input
                  type="password"
                  class="form-control"
                  v-model="passwordForm.confirm_password"
                  placeholder="********"
                />
              </div>
            </div>

            <div class="text-end mt-3">
              <button
                class="btn btn-outline-secondary me-2"
                @click="resetPasswordForm"
              >
                Cancel
              </button>

              <button
                class="btn btn-primary"
                @click="updatePassword"
                :disabled="changingPassword"
              >
                {{ changingPassword ? "Updating..." : "Update Password" }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api";
import { useRouter } from "vue-router";

const user = ref(null);

const editMode = ref(false);

const changingPassword = ref(false);

const savingProfile = ref(false);

const notification = ref({
  show: false,
  type: "success",
  message: "",
});

const profileForm = ref({
  nama_lengkap: "",
  username: "",
  email: "",
  nomor_telepon: "",
  institusi: "",
});

const showAlert = (type, message) => {
  notification.value = {
    show: true,
    type,
    message,
  };

  setTimeout(() => {
    notification.value.show = false;
  }, 3000);
};

const passwordForm = ref({
  current_password: "",
  new_password: "",
  confirm_password: "",
});

const loading = ref(true);

const loadProfile = async () => {
  try {
    const response = await api.get("/profile");

    user.value = response.data.data;
    profileForm.value = {
      nama_lengkap: user.value.nama_lengkap,
      username: user.value.username,
      email: user.value.email,
      nomor_telepon: user.value.nomor_telepon,
      institusi: user.value.institusi,
    };
  } catch (error) {
    showAlert("danger", error.response?.data?.message || "Gagal memuat profil");
  } finally {
    loading.value = false;
  }
};

const saveProfile = async () => {
  try {
    savingProfile.value = true;

    // Payload yang akan dikirim ke backend
    const payload = {
      nama_lengkap: profileForm.value.nama_lengkap,
      username: profileForm.value.username,
      email: profileForm.value.email,
      nomor_telepon: profileForm.value.nomor_telepon,
    };

    // Hanya admin yang boleh mengirim institusi
    if (user.value.role !== "nasabah") {
      payload.institusi = profileForm.value.institusi;
    }

    const response = await api.put("/profile", payload);

    user.value = response.data.data;

    localStorage.setItem("user", JSON.stringify(response.data.data));

    editMode.value = false;

    showAlert("success", response.data.message);
  } catch (error) {
    showAlert(
      "danger",
      error.response?.data?.message || "Gagal memperbarui profil",
    );
  } finally {
    savingProfile.value = false;
  }
};

const toggleEdit = () => {
  if (editMode.value) {
    profileForm.value = {
      nama_lengkap: user.value.nama_lengkap,
      username: user.value.username,
      email: user.value.email,
      nomor_telepon: user.value.nomor_telepon,
      institusi: user.value.institusi,
    };
  }

  editMode.value = !editMode.value;
};

const updatePassword = async () => {
  if (
    !passwordForm.value.current_password ||
    !passwordForm.value.new_password ||
    !passwordForm.value.confirm_password
  ) {
    showAlert("warning", "Semua field password wajib diisi");
    return;
  }

  if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
    showAlert("danger", "Konfirmasi password tidak sama");
    return;
  }

  if (passwordForm.value.new_password.length < 8) {
    showAlert("warning", "Password minimal 8 karakter");
    return;
  }

  try {
    changingPassword.value = true;

    const response = await api.put("/profile/change-password", {
      current_password: passwordForm.value.current_password,
      new_password: passwordForm.value.new_password,
      confirm_password: passwordForm.value.confirm_password,
    });

    // Kosongkan form
    passwordForm.value = {
      current_password: "",
      new_password: "",
      confirm_password: "",
    };

    showAlert("success", response.data.message);
  } catch (error) {
    console.error(error);
    console.error(error.response?.data);

    showAlert(
      "danger",
      error.response?.data?.message || "Gagal mengubah password",
    );
  } finally {
    changingPassword.value = false;
  }
};

const resetPasswordForm = () => {
  passwordForm.value = {
    current_password: "",
    new_password: "",
    confirm_password: "",
  };
};

onMounted(() => {
  loadProfile();
});

const router = useRouter();

const goBack = () => {
  router.back();
};
</script>

<style scoped>
.profile-card {
  min-height: 650px;
}

.avatar-box {
  width: 100px;
  height: 100px;

  border-radius: 50%;

  background: #0d6efd;
  color: white;

  font-size: 36px;
  font-weight: bold;

  display: flex;
  align-items: center;
  justify-content: center;
}

.card {
  border: none;
  border-radius: 15px;
}

.form-control {
  background: #f8f9fa;
}
</style>
