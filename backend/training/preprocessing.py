# ==========================================================
# IMPORT LIBRARY
# ==========================================================
import numpy as np
import pandas as pd

import os
import warnings

warnings.filterwarnings("ignore")


def main():
    # ==========================================================
    # PATH CONFIG
    # ==========================================================
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

    BACKEND_DIR = os.path.dirname(CURRENT_DIR)

    DATASET_DIR = os.path.join(BACKEND_DIR, "dataset")

    ML_PATH = os.path.join(BACKEND_DIR, "ml")

    os.makedirs(ML_PATH, exist_ok=True)

    # =====================================================
    # LOAD DATA
    # =====================================================
    DATA_PATH = os.path.join(DATASET_DIR, "data-training.csv")

    # Membuat folder ml jika belum ada
    os.makedirs(ML_PATH, exist_ok=True)

    # ==========================================================
    # LOAD DATA
    # ==========================================================

    df = pd.read_csv(DATA_PATH, delimiter=";")

    # ==========================================

    # HAPUS KOLOM NOMOR URUT
    # ==========================================

    if "No" in df.columns:
        df = df.drop(columns=["No"])

    print("Shape awal :", df.shape)
    print(df.head())

    # ==========================================================
    # RENAME
    # ==========================================================
    rename_map = {
        "SeriousDlqin2yrs": "target",
        "RevolvingUtilizationOfUnsecuredLines": "revolving_utilization",
        "NumberOfTime30-59DaysPastDueNotWorse": "delinquency_30_59",
        "DebtRatio": "debt_ratio",
        "MonthlyIncome": "monthly_income",
        "NumberOfOpenCreditLinesAndLoans": "num_credit_lines",
        "NumberOfTimes90DaysLate": "delinquency_90",
        "NumberRealEstateLoansOrLines": "real_estate_loans",
        "NumberOfTime60-89DaysPastDueNotWorse": "delinquency_60_89",
        "NumberOfDependents": "dependents",
    }
    df = df.rename(columns=rename_map)

    if "No" in df.columns:
        df = df.drop(columns=["No"])

    for c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    print(df.info())

    # ==========================================================
    # DATA QUALITY
    # ==========================================================
    quality = pd.DataFrame(
        {
            "missing": df.isna().sum(),
            "missing_%": round(df.isna().mean() * 100, 2),
            "dtype": df.dtypes.astype(str),
        }
    )
    print(quality)

    # ==========================================================
    # IMPUTATION
    # ==========================================================
    median_cols = [
        "revolving_utilization",
        "debt_ratio",
        "monthly_income",
        "dependents",
    ]
    for c in median_cols:
        df[c] = df[c].fillna(df[c].median())

    df = df.fillna(0)

    # ==========================================================
    # REMOVE DUPLICATE
    # ==========================================================
    print("Duplicate :", df.duplicated().sum())
    df = df.drop_duplicates()

    # ==========================================================
    # REMOVE INVALID AGE
    # ==========================================================
    df = df[df["age"] >= 18]

    # ==========================================================
    # IQR OUTLIER TREATMENT
    # ==========================================================
    iqr_cols = ["monthly_income", "debt_ratio", "revolving_utilization"]

    for c in iqr_cols:
        q1 = df[c].quantile(0.25)
        q3 = df[c].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        df[c] = np.clip(df[c], lower, upper)

    # Khusus revolving utilization
    df["revolving_utilization"] = df["revolving_utilization"].clip(0, 1)

    for c in ["delinquency_30_59", "delinquency_60_89", "delinquency_90"]:
        df[c] = df[c].clip(0, 10)

    # ==========================================================
    # FEATURE ENGINEERING
    # ==========================================================
    df["monthly_income_log"] = np.log1p(df["monthly_income"])
    df["delinquency_total"] = (
        df["delinquency_30_59"] + df["delinquency_60_89"] + df["delinquency_90"]
    )

    df["income_per_dependent"] = df["monthly_income"] / (df["dependents"] + 1)
    df["loan_per_age"] = df["num_credit_lines"] / (df["age"] + 1)
    df["debt_per_income"] = df["debt_ratio"] / (df["monthly_income_log"] + 1)
    df["utilization_income_ratio"] = df["revolving_utilization"] / (
        df["monthly_income_log"] + 1
    )

    # ==========================================================
    # EDA
    # ==========================================================
    print(df.describe())

    print(df["target"].value_counts())

    df["target"].value_counts().plot(kind="bar", title="Target Distribution")

    num = df.select_dtypes(include=np.number)

    corr = num.corr()

    # Histogram semua fitur
    num.hist(figsize=(18, 18))

    # Boxplot fitur utama
    for c in ["monthly_income", "debt_ratio", "revolving_utilization"]:
        df.boxplot(column=c, by="target", figsize=(8, 5))

    # ==========================================================
    # SAVE
    # ==========================================================

    df.to_csv(os.path.join(ML_PATH, "processed_dataset_v3.csv"), index=False)

    corr.to_csv(os.path.join(ML_PATH, "feature_correlation_v3.csv"))

    df.describe().T.to_csv(os.path.join(ML_PATH, "eda_summary_v3.csv"))

    quality.to_csv(os.path.join(ML_PATH, "data_quality_report.csv"))

    print("\nSemua file berhasil disimpan pada:")
    print(os.path.abspath(ML_PATH))

    print("\nGenerated Files:")
    print("- processed_dataset_v3.csv")
    print("- feature_correlation_v3.csv")
    print("- eda_summary_v3.csv")
    print("- data_quality_report.csv")
    print("======================================")


if __name__ == "__main__":
    main()
