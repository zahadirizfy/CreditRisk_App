from .preprocessing import main as preprocessing
from .feature_selection import main as feature_selection
from .train_logistic import main as logistic
from .train_knn import main as knn
from .hybrid_test import main as hybrid

from utils.retrain_status import (
    update_status,
    finish_status,
    failed_status,
)


def retrain_model():

    try:
        # =====================================================
        # STEP 1
        # =====================================================

        update_status(
            step=1,
            total_step=6,
            message="Preprocessing Dataset",
        )

        print("========== STEP 1 ==========")
        preprocessing()

        # =====================================================
        # STEP 2
        # =====================================================

        update_status(
            step=2,
            total_step=6,
            message="Feature Selection",
        )

        print("========== STEP 2 ==========")
        feature_selection()

        # =====================================================
        # STEP 3
        # =====================================================

        update_status(
            step=3,
            total_step=6,
            message="Training Logistic Regression",
        )

        print("========== STEP 3 ==========")
        logistic()

        # =====================================================
        # STEP 4
        # =====================================================

        update_status(
            step=4,
            total_step=6,
            message="Training KNN",
        )

        print("========== STEP 4 ==========")
        knn()

        # =====================================================
        # STEP 5
        # =====================================================

        update_status(
            step=5,
            total_step=6,
            message="Hybrid Evaluation",
        )

        print("========== STEP 5 ==========")

        metrics = hybrid()

        # =====================================================
        # STEP 6
        # =====================================================

        update_status(
            step=6,
            total_step=6,
            message="Menyimpan Model",
        )

        finish_status()

        return {
            "success": True,
            "message": "Retraining berhasil",
            "metrics": metrics,
        }

    except Exception as e:
        failed_status(str(e))
        raise


if __name__ == "__main__":
    retrain_model()
