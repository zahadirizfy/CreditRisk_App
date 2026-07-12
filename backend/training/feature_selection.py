import os
import numpy as np
import pandas as pd
import pickle

from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import mutual_info_classif, RFE
from sklearn.linear_model import LogisticRegression
from statsmodels.stats.outliers_influence import variance_inflation_factor

import warnings

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
    DATA_PATH = os.path.join(ML_PATH, "processed_dataset_v3.csv")

    df = pd.read_csv(DATA_PATH)
    print("Shape Awal :", df.shape)

    # =====================================================
    # HAPUS FITUR REDUNDAN
    # =====================================================
    drop_features = [
        "monthly_income",
        "delinquency_30_59",
        "delinquency_60_89",
        "delinquency_90",
    ]

    df = df.drop(columns=drop_features)

    print("Shape Setelah Drop :", df.shape)

    target = "target"
    features = [c for c in df.columns if c != target]

    X = df[features]
    y = df[target]

    # =====================================================
    # CORRELATION
    # =====================================================
    corr = df.corr(numeric_only=True)

    

    corr_target = corr["target"].drop("target").abs().sort_values(ascending=False)
    corr_target.to_csv(os.path.join(ML_PATH, "feature_correlation_target.csv"))

    # =====================================================
    # STANDARD SCALER
    # =====================================================
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

    # =====================================================
    # VIF
    # =====================================================
    vif = pd.DataFrame(
        {
            "Feature": X_scaled.columns,
            "VIF": [
                variance_inflation_factor(X_scaled.values, i)
                for i in range(X_scaled.shape[1])
            ],
        }
    ).sort_values("VIF", ascending=False)

    print(vif)
    vif.to_csv(os.path.join(ML_PATH, "vif_report.csv"), index=False)

    # =====================================================
    # MUTUAL INFORMATION
    # =====================================================
    mi = mutual_info_classif(X, y, random_state=42)

    mi_df = pd.DataFrame({"Feature": X.columns, "MI": mi}).sort_values(
        "MI", ascending=False
    )


    mi_df.to_csv(os.path.join(ML_PATH, "mutual_information.csv"), index=False)

    # =====================================================
    # RFE
    # =====================================================
    lr = LogisticRegression(max_iter=5000)

    rfe = RFE(estimator=lr, n_features_to_select=10)

    rfe.fit(X_scaled, y)

    rfe_df = pd.DataFrame(
        {"Feature": X.columns, "Selected": rfe.support_, "Ranking": rfe.ranking_}
    ).sort_values(["Ranking", "Feature"])

    rfe_df.to_csv(os.path.join(ML_PATH, "rfe_result.csv"), index=False)

    # =====================================================
    # LOGISTIC COEFFICIENT
    # =====================================================
    lr.fit(X_scaled, y)

    coef_df = pd.DataFrame(
        {
            "Feature": X.columns,
            "Coefficient": lr.coef_[0],
            "AbsCoefficient": np.abs(lr.coef_[0]),
        }
    ).sort_values("AbsCoefficient", ascending=False)

    coef_df.to_csv(os.path.join(ML_PATH, "logistic_coefficients.csv"), index=False)

    # =====================================================
    # SUMMARY TABLE
    # =====================================================
    summary = (
        corr_target.rename("Correlation")
        .reset_index()
        .rename(columns={"index": "Feature"})
    )

    summary = summary.merge(mi_df, on="Feature")
    summary = summary.merge(vif, on="Feature")
    summary = summary.merge(rfe_df[["Feature", "Selected"]], on="Feature")

    summary["Status"] = summary["Selected"].map(
        {True: "Dipakai", False: "Tidak Dipakai"}
    )

    summary = summary.sort_values(
        ["Selected", "MI", "Correlation"], ascending=[False, False, False]
    )

    print(summary)

    summary.to_csv(os.path.join(ML_PATH, "feature_selection_summary.csv"), index=False)

    # =====================================================
    # FINAL FEATURES
    # =====================================================
    selected = summary.loc[summary["Status"] == "Dipakai", "Feature"].tolist()
    # =====================================================
    # HAPUS FITUR YANG MASIH MEMILIKI MULTIKOLINEARITAS
    # =====================================================
    remove_features = ["debt_per_income"]

    selected = [f for f in selected if f not in remove_features]

    print("\nFINAL FEATURES")
    for i, f in enumerate(selected, 1):
        print(f"{i}. {f}")

    pd.DataFrame({"Feature": selected}).to_csv(
        os.path.join(ML_PATH, "selected_features.csv"), index=False
    )

    pickle.dump(selected, open(os.path.join(ML_PATH, "selected_features.pkl"), "wb"))

    print("\n====================================")
    print("Notebook 2 selesai.")
    print(f"Jumlah fitur terpilih : {len(selected)}")

    print("\nFinal Features")

    for i, f in enumerate(selected, 1):
        print(f"{i}. {f}")

    print("\nOutput berhasil disimpan pada:")
    print(os.path.abspath(ML_PATH))
    print("====================================")


if __name__ == "__main__":
    main()
