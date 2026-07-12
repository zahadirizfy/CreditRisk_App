import os
import pickle
import numpy as np
import pandas as pd

# ==========================================================
# BASE DIRECTORY
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ==========================================================
# LOAD MODEL
# ==========================================================

with open(os.path.join(BASE_DIR, "logreg_gate.pkl"), "rb") as f:
    logreg_model = pickle.load(f)

with open(os.path.join(BASE_DIR, "knn_risk.pkl"), "rb") as f:
    knn_model = pickle.load(f)

with open(os.path.join(BASE_DIR, "scaler_gate.pkl"), "rb") as f:
    scaler_gate = pickle.load(f)

with open(os.path.join(BASE_DIR, "scaler_knn.pkl"), "rb") as f:
    scaler_knn = pickle.load(f)

with open(os.path.join(BASE_DIR, "gate_features.pkl"), "rb") as f:
    gate_features = pickle.load(f)

with open(os.path.join(BASE_DIR, "knn_features.pkl"), "rb") as f:
    knn_features = pickle.load(f)

with open(os.path.join(BASE_DIR, "threshold.pkl"), "rb") as f:
    THRESHOLD = float(pickle.load(f))


KNN_K_VALUE = knn_model.n_neighbors

MODEL_INFO = {
    "gate_features": len(gate_features),
    "knn_features": len(knn_features),
    "threshold": THRESHOLD,
    "knn_k": KNN_K_VALUE,
}


# ==========================================================
# FEATURE ENGINEERING
# ==========================================================


def build_features(data):

    monthly_income = max(float(data["monthly_income"]), 0)

    dependents = max(int(data["dependents"]), 0)

    df = pd.DataFrame([data]).copy()

    df["monthly_income_log"] = np.log1p(monthly_income)

    df["delinquency_total"] = (
        df["delinquency_30_59"] + df["delinquency_60_89"] + df["delinquency_90"]
    )

    df["income_per_dependent"] = monthly_income / (dependents + 1)

    df["loan_per_age"] = df["num_credit_lines"] / (df["age"] + 1)

    df["debt_per_income"] = df["debt_ratio"] / (df["monthly_income_log"] + 1)

    df["utilization_income_ratio"] = df["revolving_utilization"] / (
        df["monthly_income_log"] + 1
    )

    return df


# ==========================================================
# HYBRID PREDICTION
# ==========================================================


def predict_risk_hybrid(nasabah):

    try:
        required_fields = [
            "revolving_utilization",
            "age",
            "delinquency_30_59",
            "debt_ratio",
            "monthly_income",
            "num_credit_lines",
            "delinquency_90",
            "real_estate_loans",
            "delinquency_60_89",
            "dependents",
        ]

        for field in required_fields:
            if field not in nasabah or nasabah[field] is None:
                return {"success": False, "message": f"Field '{field}' wajib diisi."}

        df = build_features(nasabah)

        # ======================================================
        # LOGISTIC GATE
        # ======================================================

        gate_input = df[gate_features]

        gate_scaled = scaler_gate.transform(gate_input)

        probability = float(logreg_model.predict_proba(gate_scaled)[0][1])

        # ======================================================
        # TIDAK LAYAK
        # ======================================================

        if probability >= THRESHOLD:
            return {
                "success": True,
                "status": "TIDAK LAYAK",
                "status_code": 0,
                "probability": probability,
                "risk_level": None,
                "risk_code": None,
                "risk_probability": None,
                "recommended_plafond": None,
                "recommendation": "Pengajuan kredit tidak direkomendasikan.",
                "color": "red",
                "knn_k_value": None,
            }

        # ======================================================
        # KNN RISK
        # ======================================================

        knn_input = df[knn_features]

        knn_scaled = scaler_knn.transform(knn_input)

        risk_prediction = int(knn_model.predict(knn_scaled)[0])

        risk_probability = float(knn_model.predict_proba(knn_scaled)[0][1])

        if risk_prediction == 0:
            risk_level = "RENDAH"

            risk_code = 0

            plafond = "> Rp100.000.000"

            recommendation = "Pengajuan kredit disetujui dengan risiko rendah."

            color = "green"

        else:
            risk_level = "TINGGI"

            risk_code = 1

            plafond = "≤ Rp50.000.000"

            recommendation = "Pengajuan kredit layak dipertimbangkan, namun memerlukan analisis lanjutan karena tingkat risiko relatif tinggi."

            color = "orange"

        return {
            "success": True,
            "status": "LAYAK",
            "status_code": 1,
            "probability": probability,
            "risk_level": risk_level,
            "risk_code": risk_code,
            "risk_probability": risk_probability,
            "threshold": THRESHOLD,
            "recommended_plafond": plafond,
            "recommendation": recommendation,
            "color": color,
            "knn_k_value": KNN_K_VALUE,
            "delinquency_total": int(df["delinquency_total"].iloc[0]),
        }

    except Exception as e:
        return {"success": False, "message": str(e)}
