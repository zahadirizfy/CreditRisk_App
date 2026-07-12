import os
import json
import pandas as pd

from sqlalchemy import func

from database.db import db
from models.user import User
from models.prediction import Prediction


# =====================================================
# PATH
# =====================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ML_PATH = os.path.join(BASE_DIR, "ml")


# =====================================================
# DASHBOARD SERVICE
# =====================================================


def dashboard_service():

    # =====================================================
    # TOTAL USER
    # =====================================================

    total_user = User.query.count()

    # =====================================================
    # TOTAL PREDIKSI
    # =====================================================

    total_prediction = Prediction.query.count()

    # =====================================================
    # DISTRIBUSI USER
    # =====================================================

    role_result = (
        db.session.query(
            User.role,
            func.count(User.id_user),
        )
        .group_by(User.role)
        .all()
    )

    user_distribution = {}

    for role, total in role_result:
        user_distribution[role] = total

    # =====================================================
    # AKTIVITAS PREDIKSI BULANAN
    # =====================================================

    prediction_result = (
        db.session.query(
            func.month(Prediction.prediction_date),
            func.count(Prediction.id_prediction),
        )
        .group_by(func.month(Prediction.prediction_date))
        .order_by(func.month(Prediction.prediction_date))
        .all()
    )

    month_name = [
        "",
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "Mei",
        "Jun",
        "Jul",
        "Agu",
        "Sep",
        "Okt",
        "Nov",
        "Des",
    ]

    monthly_prediction = []

    for month, total in prediction_result:
        monthly_prediction.append(
            {
                "month": month_name[int(month)],
                "total": int(total),
            }
        )

    # =====================================================
    # STATUS MODEL
    # =====================================================

    status_file = os.path.join(
        ML_PATH,
        "retrain_status.json",
    )

    last_retrain = "-"

    if os.path.exists(status_file):
        try:
            with open(status_file, "r", encoding="utf-8") as f:
                status_data = json.load(f)

            # kalau nanti kita tambahkan updated_at
            last_retrain = status_data.get("updated_at", "-")

        except Exception:
            last_retrain = "-"

    model_status = {
        "model": "Hybrid Logistic Regression + KNN",
        "status": "🟢 Model Ready",
        "last_retrain": last_retrain,
    }

    # =====================================================
    # DATASET
    # =====================================================

    training_dataset = 0

    processed_dataset = os.path.join(
        ML_PATH,
        "processed_dataset_v3.csv",
    )

    if os.path.exists(processed_dataset):
        training_dataset = len(pd.read_csv(processed_dataset))

    # =====================================================
    # EVALUASI MODEL
    # =====================================================

    evaluation = {}

    summary_file = os.path.join(
        ML_PATH,
        "logistic_experiment_summary_final.csv",
    )

    if os.path.exists(summary_file):
        df = pd.read_csv(summary_file)

        best = df.sort_values("F1", ascending=False).iloc[0]

        evaluation = {
            "accuracy": float(best["Accuracy"]),
            "precision": float(best["Precision"]),
            "recall": float(best["Recall"]),
            "f1": float(best["F1"]),
            "roc_auc": float(best["ROC_AUC"]),
        }

    # =====================================================
    # RESPONSE
    # =====================================================

    return {
        "total_user": total_user,
        "total_prediction": total_prediction,
        "user_distribution": user_distribution,
        "monthly_prediction": monthly_prediction,
        "model_status": model_status,
        "dataset": {
            "name": "processed_dataset_v3.csv",
            "original": 150000,
            "training": training_dataset,
            "url": "https://www.kaggle.com/c/GiveMeSomeCredit",
        },
        "evaluation": evaluation,
    }
