import os
import pickle
import warnings

import pandas as pd

from imblearn.over_sampling import SMOTE
from sklearn.feature_selection import mutual_info_classif
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")


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
    df = pd.read_csv(os.path.join(ML_PATH, "processed_dataset_v3.csv"))

    # Hanya data yang layak untuk klasifikasi risiko
    df = df[df["target"] == 0].copy()

    # =====================================================
    # MEMBENTUK RISK LABEL
    # =====================================================
    risk_cols = [
        "delinquency_total",
        "debt_ratio",
        "revolving_utilization",
        "monthly_income_log",
    ]

    risk_scaled = StandardScaler().fit_transform(df[risk_cols])

    risk_scaled = pd.DataFrame(
        risk_scaled,
        columns=risk_cols,
        index=df.index,
    )

    df["risk_index"] = (
        0.40 * risk_scaled["delinquency_total"]
        + 0.25 * risk_scaled["debt_ratio"]
        + 0.25 * risk_scaled["revolving_utilization"]
        - 0.10 * risk_scaled["monthly_income_log"]
    )

    threshold = df["risk_index"].quantile(0.75)

    df["risk_label"] = (df["risk_index"] >= threshold).astype(int)

    print(df["risk_label"].value_counts())

    # =====================================================
    # FEATURE KNN
    # =====================================================
    knn_features = [
        "revolving_utilization",
        "delinquency_total",
        "monthly_income_log",
        "income_per_dependent",
        "debt_ratio",
        "loan_per_age",
        "real_estate_loans",
        "age",
        "utilization_income_ratio",
    ]

    X = df[knn_features]
    y = df["risk_label"]

    # =====================================================
    # SPLIT DATA
    # =====================================================
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        stratify=y,
        random_state=42,
    )

    scaler = StandardScaler()

    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # =====================================================
    # SMOTE
    # =====================================================
    X_train, y_train = SMOTE(
        random_state=42,
        sampling_strategy=1.0,
    ).fit_resample(X_train, y_train)

    print("\nDistribusi setelah SMOTE")
    print(pd.Series(y_train).value_counts())

    # =====================================================
    # TRAIN MODEL
    # =====================================================
    print("=" * 80)
    print("TRAINING KNN")
    print("=" * 80)

    best_params = {
        "n_neighbors": 3,
        "weights": "distance",
        "metric": "manhattan",
    }

    model = KNeighborsClassifier(**best_params)

    model.fit(X_train, y_train)

    print("TRAINING KNN SELESAI")

    # =====================================================
    # EVALUASI
    # =====================================================
    prediction = model.predict(X_test)

    probability = model.predict_proba(X_test)[:, 1]

    print(classification_report(y_test, prediction))

    print(confusion_matrix(y_test, prediction))

    print("Accuracy :", accuracy_score(y_test, prediction))
    print("Precision:", precision_score(y_test, prediction))
    print("Recall   :", recall_score(y_test, prediction))
    print("F1 Score :", f1_score(y_test, prediction))
    print("ROC AUC  :", roc_auc_score(y_test, probability))

    # =====================================================
    # FEATURE IMPORTANCE
    # =====================================================
    importance = mutual_info_classif(
        X,
        y,
        random_state=42,
    )

    importance_df = pd.DataFrame(
        {
            "Feature": knn_features,
            "Importance": importance,
        }
    ).sort_values(
        by="Importance",
        ascending=False,
    )

    print(importance_df)

    # =====================================================
    # SAVE MODEL
    # =====================================================
    pickle.dump(
        model,
        open(os.path.join(ML_PATH, "knn_risk.pkl"), "wb"),
    )

    pickle.dump(
        scaler,
        open(os.path.join(ML_PATH, "scaler_knn.pkl"), "wb"),
    )

    pickle.dump(
        knn_features,
        open(os.path.join(ML_PATH, "knn_features.pkl"), "wb"),
    )

    pickle.dump(
        threshold,
        open(os.path.join(ML_PATH, "risk_threshold.pkl"), "wb"),
    )

    pickle.dump(
        best_params,
        open(os.path.join(ML_PATH, "knn_best_params.pkl"), "wb"),
    )

    # =====================================================
    # SAVE REPORT
    # =====================================================
    importance_df.to_csv(
        os.path.join(ML_PATH, "knn_feature_importance.csv"),
        index=False,
    )

    df.to_csv(
        os.path.join(ML_PATH, "risk_label_dataset.csv"),
        index=False,
    )

    summary = pd.DataFrame(
        {
            "Accuracy": [accuracy_score(y_test, prediction)],
            "Precision": [precision_score(y_test, prediction)],
            "Recall": [recall_score(y_test, prediction)],
            "F1": [f1_score(y_test, prediction)],
            "ROC_AUC": [roc_auc_score(y_test, probability)],
            "Best_Params": [str(best_params)],
        }
    )

    summary.to_csv(
        os.path.join(ML_PATH, "knn_summary.csv"),
        index=False,
    )

    # =====================================================
    # FINISH
    # =====================================================
    print("=" * 80)
    print("Notebook 4 selesai.")
    print("Best Params :", best_params)
    print("Output berhasil disimpan pada:")
    print(os.path.abspath(ML_PATH))
    print("=" * 80)


if __name__ == "__main__":
    main()