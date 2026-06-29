import pickle
import pandas as pd
import numpy as np
import os

# ==========================================
# BASE DIRECTORY
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ==========================================
# LOAD MODEL
# ==========================================

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
    THRESHOLD = pickle.load(f)

KNN_K_VALUE = knn_model.n_neighbors


print("\nKNN FEATURES")
print(knn_features)

# ==========================================
# PREDICT HYBRID
# ==========================================


def predict_risk_hybrid(nasabah):

    try:
        # ==========================================
        # VALIDASI INPUT
        # ==========================================

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
            if field not in nasabah:
                return {"success": False, "message": f"Field {field} wajib diisi"}

        # ==========================================
        # PREPARE DATA
        # ==========================================

        monthly_income = max(0, float(nasabah["monthly_income"]))

        dependents = max(1, int(nasabah["dependents"]))

        df_input = pd.DataFrame([nasabah])

        # ==========================================
        # FEATURE ENGINEERING
        # ==========================================

        df_input["monthly_income_log"] = np.log1p(monthly_income)

        df_input["delinquency_total"] = (
            df_input["delinquency_30_59"]
            + df_input["delinquency_60_89"]
            + df_input["delinquency_90"]
        )

        df_input["income_per_dependent"] = monthly_income / (dependents + 1)

        df_input["credit_per_age"] = df_input["num_credit_lines"] / (
            df_input["age"] + 1
        )

        df_input["debt_per_income"] = df_input["debt_ratio"] / (
            df_input["monthly_income_log"] + 1
        )

        df_input["delinquency_ratio"] = df_input["delinquency_total"] / (
            df_input["num_credit_lines"] + 1
        )

        df_input["income_credit_ratio"] = df_input["monthly_income_log"] / (
            df_input["num_credit_lines"] + 1
        )

        df_input["delinquency_income_ratio"] = df_input["delinquency_total"] / (
            df_input["monthly_income_log"] + 1
        )

        # ==========================================
        # PREPARE LOGISTIC FEATURES
        # ==========================================

        X_gate_input = pd.DataFrame()

        for feature in gate_features:
            if feature in df_input.columns:
                X_gate_input[feature] = [df_input[feature].values[0]]

            else:
                X_gate_input[feature] = [0]

        # ==========================================
        # LOGISTIC REGRESSION
        # ==========================================

        X_gate_scaled = scaler_gate.transform(X_gate_input)

        probability = float(logreg_model.predict_proba(X_gate_scaled)[0][1])

        print("\n========== DEBUG LOGREG ==========")
        print(X_gate_input)
        print("\nProbability :", probability)
        print("Threshold   :", THRESHOLD)
        print("==================================")

        # ==========================================
        # TIDAK LAYAK
        # ==========================================

        if probability >= THRESHOLD:
            return {
                "success": True,
                "status": "TIDAK LAYAK",
                "status_code": 0,
                "probability": probability,
                "risk_level": None,
                "risk_code": None,
                "risk_probability": None,
                "risk_score": None,
                "knn_k_value": None,
                "recommended_plafond": None,
                "recommendation": "Pengajuan kredit tidak direkomendasikan.",
                "color": "red",
            }

        # ==========================================
        # KNN INPUT
        # ==========================================

        knn_input = pd.DataFrame(
            [
                {
                    "debt_ratio": nasabah["debt_ratio"],
                    "revolving_utilization": nasabah["revolving_utilization"],
                    "monthly_income_log": np.log1p(monthly_income),
                    "age": nasabah["age"],
                    "num_credit_lines": nasabah["num_credit_lines"],
                    "delinquency_total": int(df_input["delinquency_total"].values[0]),
                    "dependents": nasabah["dependents"],
                }
            ]
        )

        print("\nKNN INPUT RAW")
        print(knn_input)

        X_knn_scaled = scaler_knn.transform(knn_input)

        print("\nKNN INPUT SCALED")
        print(X_knn_scaled)

        

        risk_probability = float(knn_model.predict_proba(X_knn_scaled)[0][1])

        print(knn_model.predict(X_knn_scaled))

        print(knn_model.predict_proba(X_knn_scaled))

        print("\nRisk Probability:")
        print(risk_probability)
        print("================================")

        # ==========================================
        # RISK LEVEL
        # ==========================================

        if risk_probability < 0.50:
            risk_level = "RENDAH"
            risk_code = 0

            plafond = "> Rp 100.000.000"

            recommendation = "Pengajuan kredit disetujui dengan risiko rendah."

            color = "green"

        else:
            risk_level = "TINGGI"
            risk_code = 1

            plafond = "≤ Rp 50.000.000"

            recommendation = "Pengajuan kredit disetujui dengan risiko tinggi."

            color = "orange"

        # ==========================================
        # RETURN RESULT
        # ==========================================

        return {
            "success": True,
            "status": "LAYAK",
            "status_code": 1,
            "probability": probability,
            "risk_level": risk_level,
            "risk_code": risk_code,
            "risk_probability": risk_probability,
            "delinquency_total": int(df_input["delinquency_total"].values[0]),
            "knn_k_value": KNN_K_VALUE,
            "recommended_plafond": plafond,
            "recommendation": recommendation,
            "color": color,
        }

    except Exception as e:
        return {"success": False, "message": str(e)}
