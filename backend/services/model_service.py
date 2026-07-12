import os

from werkzeug.utils import secure_filename

from training.run_training import retrain_model
from services.dataset_validator import validate_dataset

# =====================================================
# PATH CONFIG
# =====================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ML_PATH = os.path.join(BASE_DIR, "ml")

os.makedirs(ML_PATH, exist_ok=True)

DATASET_PATH = os.path.join(ML_PATH, "processed_dataset_v3.csv")

# =====================================================
# STATUS RETRAIN
# =====================================================

retrain_status = {
    "status": "idle",
    "step": 0,
    "total_step": 6,
    "message": "Belum ada proses.",
}

# =====================================================
# UPDATE STATUS
# =====================================================


def update_retrain_status(step, message, status="running"):
    retrain_status["status"] = status
    retrain_status["step"] = step
    retrain_status["message"] = message


# =====================================================
# GET STATUS
# =====================================================


def get_retrain_status():
    return retrain_status


# =====================================================
# ALLOWED FILE
# =====================================================

ALLOWED_EXTENSIONS = {"csv"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# =====================================================
# RETRAIN SERVICE
# =====================================================


def retrain_service(file):

    # Reset Status
    update_retrain_status(
        0,
        "Memulai proses retraining...",
        "running",
    )

    # ==========================================
    # FILE KOSONG
    # ==========================================

    if file is None:
        update_retrain_status(
            0,
            "Dataset belum dipilih.",
            "failed",
        )

        return {
            "success": False,
            "message": "Dataset belum dipilih.",
        }

    # ==========================================
    # EXTENSION
    # ==========================================

    if not allowed_file(file.filename):
        update_retrain_status(
            0,
            "File harus CSV.",
            "failed",
        )

        return {
            "success": False,
            "message": "File harus berformat CSV.",
        }

    # ==========================================
    # SIMPAN FILE
    # ==========================================

    filename = secure_filename(file.filename)

    temp_path = os.path.join(
        ML_PATH,
        filename,
    )

    file.save(temp_path)

    # ==========================================
    # VALIDASI
    # ==========================================

    update_retrain_status(
        1,
        "Validasi dataset...",
    )

    valid, result = validate_dataset(temp_path)

    if not valid:
        os.remove(temp_path)

        update_retrain_status(
            0,
            result,
            "failed",
        )

        return {
            "success": False,
            "message": result,
        }

    # ==========================================
    # GANTI DATASET
    # ==========================================

    if os.path.exists(DATASET_PATH):
        os.remove(DATASET_PATH)

    os.rename(
        temp_path,
        DATASET_PATH,
    )

    # ==========================================
    # RETRAIN
    # ==========================================

    update_retrain_status(
        2,
        "Menjalankan training model...",
    )

    try:
        training_result = retrain_model()

        update_retrain_status(
            6,
            "Retraining selesai.",
            "success",
        )

        return {
            "success": True,
            "message": "Retraining model berhasil.",
            "dataset": {
                "filename": filename,
                "rows": result["rows"],
                "columns": result["columns"],
            },
            "metrics": training_result["metrics"],
        }

    except Exception as e:
        update_retrain_status(
            0,
            str(e),
            "failed",
        )

        raise
