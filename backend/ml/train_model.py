import pickle
import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
    precision_recall_curve,
)

from imblearn.over_sampling import SMOTE


def train_hybrid_model_v2():

    print("Loading dataset...")

    df = pd.read_csv("dataset/data-training.csv", delimiter=";")

    # ==========================
    # RENAME COLUMN
    # ==========================

    df = df.rename(
        columns={
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
    )

    if "No" in df.columns:
        df = df.drop(columns=["No"])

        # ==========================
        # NUMERIC
        # ==========================

    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

        # ==========================
        # MISSING VALUE
        # ==========================

    df["monthly_income"] = df["monthly_income"].fillna(df["monthly_income"].median())

    df["dependents"] = df["dependents"].fillna(df["dependents"].median())

    df = df.fillna(0)

    # ==========================
    # OUTLIER
    # ==========================

    income_cap = df["monthly_income"].quantile(0.99)

    debt_cap = df["debt_ratio"].quantile(0.99)

    df["monthly_income"] = np.clip(df["monthly_income"], 0, income_cap)

    df["debt_ratio"] = np.clip(df["debt_ratio"], 0, debt_cap)

    # Revolving Utilization
    df["revolving_utilization"] = np.clip(df["revolving_utilization"], 0, 1)

    # Delinquency
    for col in ["delinquency_30_59", "delinquency_60_89", "delinquency_90"]:
        df[col] = np.clip(df[col], 0, 10)

    # ==========================
    # FEATURE ENGINEERING
    # ==========================

    df["monthly_income_log"] = np.log1p(df["monthly_income"])

    df["income_per_dependent"] = df["monthly_income"] / (df["dependents"] + 1)

    df["delinquency_total"] = (
        df["delinquency_30_59"] + df["delinquency_60_89"] + df["delinquency_90"]
    )
    df["credit_per_age"] = df["num_credit_lines"] / (df["age"] + 1)

    df["debt_per_income"] = df["debt_ratio"] / (df["monthly_income_log"] + 1)

    df["delinquency_ratio"] = df["delinquency_total"] / (df["num_credit_lines"] + 1)

    df["income_credit_ratio"] = df["monthly_income_log"] / (df["num_credit_lines"] + 1)

    df["delinquency_income_ratio"] = df["delinquency_total"] / (
        df["monthly_income_log"] + 1
    )

    # ==========================
    # LOGISTIC FEATURES
    # ==========================

    gate_features = [
        "revolving_utilization",
        "age",
        "debt_ratio",
        "monthly_income_log",
        "num_credit_lines",
        "delinquency_30_59",
        "delinquency_60_89",
        "delinquency_90",
        "real_estate_loans",
        "dependents",
        "delinquency_total",
        "income_per_dependent",
        "credit_per_age",
        "debt_per_income",
        "delinquency_ratio",
        "income_credit_ratio",
        "delinquency_income_ratio",
    ]

    # ==========================
    # LOGISTIC REGRESSION
    # ==========================

    X = df[gate_features]
    y = df["target"]

    scaler_gate = StandardScaler()

    X_scaled = scaler_gate.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )

    smote = SMOTE(random_state=42, sampling_strategy=0.3)

    X_train_bal, y_train_bal = smote.fit_resample(X_train, y_train)

    logreg_model = LogisticRegression(
        C=1.0, class_weight="balanced", max_iter=5000, random_state=42
    )

    logreg_model.fit(X_train_bal, y_train_bal)

    y_proba = (logreg_model.predict_proba(X_test))[:, 1]
    precision, recall, thresholds = precision_recall_curve(y_test, y_proba)

    f1_scores = (2 * precision * recall) / (precision + recall + 1e-10)

    best_idx = np.argmax(f1_scores)
    best_threshold = thresholds[best_idx]
    print("\nBest Threshold:", best_threshold)

    y_pred = (y_proba >= best_threshold).astype(int)

    print("\n================================")
    print("CONFUSION MATRIX")
    print("================================")

    print(confusion_matrix(y_test, y_pred))

    print("\n================================")
    print("CLASSIFICATION REPORT")
    print("================================")

    print(classification_report(y_test, y_pred))
    print("\nProbabilitas Min :", y_proba.min())
    print("Probabilitas Max :", y_proba.max())
    print("Probabilitas Mean:", y_proba.mean())

    # ==========================
    # KNN DATA
    # ==========================

    df_layak = df[df["target"] == 0].copy()

    df_layak["risk_score"] = (
        df_layak["delinquency_total"] * 5
        + df_layak["debt_ratio"] * 20
        + df_layak["revolving_utilization"] * 20
        - df_layak["monthly_income_log"]
    )

    risk_threshold = df_layak["risk_score"].quantile(0.75)

    df_layak["risk_label"] = np.where(df_layak["risk_score"] >= risk_threshold, 1, 0)

    print("\nRisk Threshold:")
    print(risk_threshold)

    print("\nDistribusi Risk Label:")
    print(df_layak["risk_label"].value_counts())

    knn_features = [
        "debt_ratio",
        "revolving_utilization",
        "monthly_income_log",
        "age",
        "num_credit_lines",
        "delinquency_total",
        "dependents",
    ]

    X_knn = df_layak[knn_features]
    y_knn = df_layak["risk_label"]

    # ==========================
    # TRAIN TEST SPLIT KNN
    # ==========================

    X_knn_train, X_knn_test, y_knn_train, y_knn_test = train_test_split(
        X_knn, y_knn, test_size=0.2, random_state=42, stratify=y_knn
    )

    print("\nTRAIN")
    print(pd.Series(y_knn_train).value_counts())

    print("\nTEST")
    print(pd.Series(y_knn_test).value_counts())

    # ==========================
    # SCALING
    # ==========================

    scaler_knn = StandardScaler()

    X_knn_train = scaler_knn.fit_transform(X_knn_train)

    X_knn_test = scaler_knn.transform(X_knn_test)

    print("\nSCALER KNN MEAN")
    print(scaler_knn.mean_)

    print("\nSCALER KNN SCALE")
    print(scaler_knn.scale_)

    # ==========================
    # SMOTE
    # ==========================

    smote_knn = SMOTE(random_state=42, sampling_strategy=1.0)

    X_knn_train, y_knn_train = smote_knn.fit_resample(X_knn_train, y_knn_train)

    # ==========================
    # GRID SEARCH
    # ==========================

    grid_search = GridSearchCV(
        KNeighborsClassifier(),
        {"n_neighbors": [3, 5, 7, 9], "weights": ["uniform", "distance"]},
        cv=5,
        scoring="f1",
    )

    grid_search.fit(X_knn_train, y_knn_train)

    knn_model = grid_search.best_estimator_

    # ==========================
    # EVALUASI KNN
    # ==========================

    y_knn_pred = knn_model.predict(X_knn_test)

    print("\n================================")
    print("KNN CONFUSION MATRIX")
    print("================================")

    print(confusion_matrix(y_knn_test, y_knn_pred))

    print("\n================================")
    print("KNN CLASSIFICATION REPORT")
    print("================================")

    print(classification_report(y_knn_test, y_knn_pred))

    # ==========================
    # SAVE MODEL
    # ==========================

    pickle.dump(logreg_model, open("ml/logreg_gate.pkl", "wb"))

    pickle.dump(knn_model, open("ml/knn_risk.pkl", "wb"))

    pickle.dump(scaler_gate, open("ml/scaler_gate.pkl", "wb"))

    pickle.dump(scaler_knn, open("ml/scaler_knn.pkl", "wb"))

    pickle.dump(gate_features, open("ml/gate_features.pkl", "wb"))

    pickle.dump(knn_features, open("ml/knn_features.pkl", "wb"))
    pickle.dump(best_threshold, open("ml/threshold.pkl", "wb"))

    return {
        "accuracy": round(accuracy_score(y_test, y_pred) * 100, 2),
        "precision": round(precision_score(y_test, y_pred) * 100, 2),
        "recall": round(recall_score(y_test, y_pred) * 100, 2),
        "f1_score": round(f1_score(y_test, y_pred) * 100, 2),
        "roc_auc": round(roc_auc_score(y_test, y_proba) * 100, 2),
        "best_knn_params": grid_search.best_params_,
    }
