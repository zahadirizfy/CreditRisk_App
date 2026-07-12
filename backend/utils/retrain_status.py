import json
import os
from datetime import datetime

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

BACKEND_DIR = os.path.dirname(CURRENT_DIR)

STATUS_FILE = os.path.join(
    BACKEND_DIR,
    "ml",
    "retrain_status.json",
)


def update_status(
    step,
    total_step,
    message,
    status="running",
    updated_at=None,
):
    """
    Menyimpan status retraining.
    """

    os.makedirs(os.path.dirname(STATUS_FILE), exist_ok=True)

    data = {
        "status": status,
        "step": step,
        "total_step": total_step,
        "message": message,
        "updated_at": updated_at or datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
    }

    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def finish_status():
    update_status(
        step=6,
        total_step=6,
        message="Retraining selesai.",
        status="success",
    )


def failed_status(message):
    update_status(
        step=0,
        total_step=6,
        message=message,
        status="failed",
    )


def get_status():

    if not os.path.exists(STATUS_FILE):
        return {
            "status": "idle",
            "step": 0,
            "total_step": 6,
            "message": "Belum ada proses.",
        }

    with open(
        STATUS_FILE,
        "r",
        encoding="utf-8",
    ) as f:
        return json.load(f)
