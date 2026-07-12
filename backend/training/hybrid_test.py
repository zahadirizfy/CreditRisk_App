import pickle
import os
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
)


def main():
    # =====================================================
    # PATH CONFIG
    # =====================================================
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

    BACKEND_DIR = os.path.dirname(CURRENT_DIR)

    ML_PATH = os.path.join(BACKEND_DIR, "ml")

    os.makedirs(ML_PATH, exist_ok=True)

    # =====================================================
    # LOAD DATA
    # =====================================================
    DATA_PATH = os.path.join(ML_PATH, "processed_dataset_v3.csv")

    # =====================================================
    # LOAD MODEL
    # =====================================================
    logreg = pickle.load(open(os.path.join(ML_PATH, "logreg_gate.pkl"), "rb"))

    gate_scaler = pickle.load(open(os.path.join(ML_PATH, "scaler_gate.pkl"), "rb"))

    gate_features = pickle.load(open(os.path.join(ML_PATH, "gate_features.pkl"), "rb"))

    threshold = pickle.load(open(os.path.join(ML_PATH, "threshold.pkl"), "rb"))

    knn = pickle.load(open(os.path.join(ML_PATH, "knn_risk.pkl"), "rb"))

    knn_scaler = pickle.load(open(os.path.join(ML_PATH, "scaler_knn.pkl"), "rb"))

    knn_features = pickle.load(open(os.path.join(ML_PATH, "knn_features.pkl"), "rb"))

    # =====================================================
    # DATA
    # =====================================================
    df = pd.read_csv(DATA_PATH)

    # =====================================================
    # HYBRID FUNCTION
    # =====================================================
    def hybrid_predict(row):

        gate = row[gate_features].to_frame().T
        gate = gate_scaler.transform(gate)

        probability = logreg.predict_proba(gate)[0, 1]

        if probability >= threshold:
            return pd.Series(
                {
                    "Probability": probability,
                    "Eligibility": "Tidak Layak",
                    "Risk": "-",
                    "Recommendation": "Kredit Ditolak",
                }
            )

        knn_input = row[knn_features].to_frame().T
        knn_input = knn_scaler.transform(knn_input)

        risk = knn.predict(knn_input)[0]

        if risk == 0:
            return pd.Series(
                {
                    "Probability": probability,
                    "Eligibility": "Layak",
                    "Risk": "Risiko Rendah",
                    "Recommendation": "Kredit Disetujui",
                }
            )

        return pd.Series(
            {
                "Probability": probability,
                "Eligibility": "Layak",
                "Risk": "Risiko Tinggi",
                "Recommendation": "Perlu Analisis Lanjutan",
            }
        )

    # =====================================================
    # DEMO SAMPLE
    # =====================================================
    sample = df.sample(20, random_state=42)
    pred = sample.apply(hybrid_predict, axis=1)

    demo = pd.concat(
        [sample.reset_index(drop=True), pred.reset_index(drop=True)], axis=1
    )

    print("\n===== HASIL SIMULASI =====")
    print(demo[["target", "Probability", "Eligibility", "Risk", "Recommendation"]])

    # =====================================================
    # LOGISTIC EVALUATION
    # =====================================================
    X = df[gate_features]
    y = df["target"]

    X_scaled = gate_scaler.transform(X)

    proba = logreg.predict_proba(X_scaled)[:, 1]
    pred_gate = (proba >= threshold).astype(int)

    acc = accuracy_score(y, pred_gate)
    pre = precision_score(y, pred_gate)
    rec = recall_score(y, pred_gate)
    f1 = f1_score(y, pred_gate)
    auc = roc_auc_score(y, proba)

    print("\n===== LOGISTIC GATE =====")
    print(classification_report(y, pred_gate))
    print(confusion_matrix(y, pred_gate))

    knn_summary = pd.read_csv(os.path.join(ML_PATH, "knn_summary.csv"))
    comparison = pd.DataFrame(
        {
            "Model": ["Logistic Regression", "KNN (Notebook 4)"],
            "Accuracy": [
                round(acc * 100, 2),
                round(knn_summary.loc[0, "Accuracy"] * 100, 2),
            ],
            "Precision": [
                round(pre * 100, 2),
                round(knn_summary.loc[0, "Precision"] * 100, 2),
            ],
            "Recall": [
                round(rec * 100, 2),
                round(knn_summary.loc[0, "Recall"] * 100, 2),
            ],
            "F1-Score": [round(f1 * 100, 2), round(knn_summary.loc[0, "F1"] * 100, 2)],
            "ROC-AUC": [
                round(auc * 100, 2),
                round(knn_summary.loc[0, "ROC_AUC"] * 100, 2),
            ],
        }
    )

    print("\n===== PERBANDINGAN MODEL =====")
    print(comparison)

    summary = (
        demo["Recommendation"]
        .value_counts()
        .rename_axis("Recommendation")
        .reset_index(name="Total")
    )
    print("\n===== RINGKASAN KEPUTUSAN =====")
    print(summary)

    demo.to_csv(os.path.join(ML_PATH, "hybrid_prediction_result.csv"), index=False)

    comparison.to_csv(os.path.join(ML_PATH, "model_comparison.csv"), index=False)
    summary.to_csv(os.path.join(ML_PATH, "hybrid_summary.csv"), index=False)

    print("\n===== HYBRID SUMMARY =====")
    print(demo["Recommendation"].value_counts())

    print("\n===== MODEL INFORMATION =====")
    print(f"Gate Features : {len(gate_features)}")
    print(f"KNN Features  : {len(knn_features)}")
    print(f"Threshold     : {threshold:.6f}")

    print("=" * 80)
    print("Notebook 5 selesai.")
    print("Output berhasil disimpan pada:")
    print(os.path.abspath(ML_PATH))
    print("=" * 80)

    # =====================================================
    # RETURN METRICS
    # =====================================================

    return {
        "accuracy": round(acc * 100, 2),
        "precision": round(pre * 100, 2),
        "recall": round(rec * 100, 2),
        "f1": round(f1 * 100, 2),
        "roc_auc": round(auc * 100, 2),
        "threshold": round(threshold, 6),
        "gate_features": len(gate_features),
        "knn_features": len(knn_features),
    }


if __name__ == "__main__":
    main()
