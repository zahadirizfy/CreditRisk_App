import os
import pickle
import numpy as np
import pandas as pd

from sklearn.model_selection import (
    train_test_split,
    GridSearchCV,
    StratifiedKFold,
)

from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression

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
    os.makedirs(ML_PATH, exist_ok=True)

    # =====================================================
    # LOAD DATA
    # =====================================================
    df = pd.read_csv(os.path.join(ML_PATH, "processed_dataset_v3.csv"))

    gate_features = pickle.load(
        open(os.path.join(ML_PATH, "selected_features.pkl"), "rb")
    )

    X = df[gate_features]
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    scaler = StandardScaler()

    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    experiments = [
        ("SMOTE_03", 0.3, None),
        ("SMOTE_05", 0.5, None),
        ("SMOTE_07", 0.7, None),
        ("SMOTE_10", 1.0, None),
        ("CLASS_WEIGHT", None, "balanced"),
    ]

    param_grid = {
        "C": [0.001, 0.01, 0.1, 1, 10, 100],
        "solver": ["lbfgs", "liblinear", "newton-cg", "saga"],
        "penalty": ["l2"],
    }

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    summary = []

    best_params = None
    best_model = None
    best_threshold = None
    best_name = ""
    best_score = -1

    for name, smote_ratio, class_weight in experiments:
        print("=" * 80)
        print(name)
        print("=" * 80)

        Xtr = X_train.copy()
        ytr = y_train.copy()

        if smote_ratio is not None:
            sm = SMOTE(sampling_strategy=smote_ratio, random_state=42)
            Xtr, ytr = sm.fit_resample(Xtr, ytr)

            print("\nDistribusi setelah SMOTE")
            print(pd.Series(ytr).value_counts())

        grid = GridSearchCV(
            LogisticRegression(
                class_weight=class_weight, max_iter=6000, random_state=42
            ),
            param_grid,
            scoring="f1",
            cv=cv,
            n_jobs=1,
        )

        grid.fit(Xtr, ytr)

        model = grid.best_estimator_

        cv_f1 = grid.best_score_

        proba = model.predict_proba(X_test)[:, 1]

        precision, recall, thresholds = precision_recall_curve(y_test, proba)

        f1 = (2 * precision * recall) / (precision + recall + 1e-9)

        idx = np.argmax(f1[:-1])
        threshold = thresholds[idx]

        pred = (proba >= threshold).astype(int)

        acc = accuracy_score(y_test, pred)
        pre = precision_score(y_test, pred)
        rec = recall_score(y_test, pred)
        f1s = f1_score(y_test, pred)
        auc = roc_auc_score(y_test, proba)

        print("Best Params :", grid.best_params_)
        print("Best Threshold :", round(threshold, 4))
        print(classification_report(y_test, pred))
        print(confusion_matrix(y_test, pred))

        summary.append(
            {
                "Model": name,
                "Accuracy": acc,
                "Precision": pre,
                "Recall": rec,
                "F1": f1s,
                "ROC_AUC": auc,
                "CV_F1": cv_f1,
                "Threshold": threshold,
                "Best_Params": str(grid.best_params_),
            }
        )

        if f1s > best_score:
            best_score = f1s
            best_model = model
            best_threshold = threshold
            best_name = name
            best_params = grid.best_params_

    summary = pd.DataFrame(summary)
    summary = summary.sort_values(["F1", "ROC_AUC"], ascending=False)

    print(summary)

    summary.to_csv(
        os.path.join(ML_PATH, "logistic_experiment_summary_final.csv"), index=False
    )

    best_proba = best_model.predict_proba(X_test)[:, 1]
    best_pred = (best_proba >= best_threshold).astype(int)

    coef_df = pd.DataFrame(
        {"Feature": gate_features, "Coefficient": best_model.coef_[0]}
    )

    coef_df.to_csv(os.path.join(ML_PATH, "logreg_coefficients.csv"), index=False)

    cm_df = pd.DataFrame(
        confusion_matrix(y_test, best_pred),
        columns=["Pred 0", "Pred 1"],
        index=["Actual 0", "Actual 1"],
    )

    cm_df.to_csv(os.path.join(ML_PATH, "logreg_confusion_matrix.csv"), index=True)

    report = classification_report(y_test, best_pred, output_dict=True)

    pd.DataFrame(report).transpose().to_csv(
        os.path.join(ML_PATH, "logreg_classification_report.csv")
    )

    pickle.dump(best_model, open(os.path.join(ML_PATH, "logreg_gate.pkl"), "wb"))

    pickle.dump(best_threshold, open(os.path.join(ML_PATH, "threshold.pkl"), "wb"))

    pickle.dump(scaler, open(os.path.join(ML_PATH, "scaler_gate.pkl"), "wb"))

    pickle.dump(gate_features, open(os.path.join(ML_PATH, "gate_features.pkl"), "wb"))

    pickle.dump(
        best_params, open(os.path.join(ML_PATH, "logreg_best_params.pkl"), "wb")
    )

    print("=" * 80)
    print(f"BEST MODEL : {best_name}")
    print(f"BEST F1    : {best_score:.4f}")
    print("=" * 80)

    print("\nModel berhasil disimpan pada:")
    print(os.path.abspath(ML_PATH))


if __name__ == "__main__":
    main()
