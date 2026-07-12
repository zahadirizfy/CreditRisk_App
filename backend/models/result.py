from database.db import db
from datetime import datetime


class Result(db.Model):
    __tablename__ = "results"

    id_result = db.Column(db.Integer, primary_key=True)

    id_prediction = db.Column(
        db.Integer,
        db.ForeignKey("predictions.id_prediction"),
        nullable=False,
        unique=True,
    )

    # ===============================
    # LOGISTIC GATE
    # ===============================
    logistic_probability = db.Column(db.Float, nullable=False)

    credit_eligibility = db.Column(db.String(20), nullable=False)

    # ===============================
    # KNN
    # ===============================
    risk_probability = db.Column(db.Float, nullable=True)

    risk_level = db.Column(db.String(20), nullable=True)

    knn_k_value = db.Column(db.Integer, nullable=True)

    # ===============================
    # RECOMMENDATION
    # ===============================
    recommendation = db.Column(db.Text, nullable=True)

    recommended_plafond = db.Column(db.String(50), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id_result": self.id_result,
            "id_prediction": self.id_prediction,
            "logistic_probability": self.logistic_probability,
            "credit_eligibility": self.credit_eligibility,
            "risk_probability": self.risk_probability,
            "risk_level": self.risk_level,
            "knn_k_value": self.knn_k_value,
            "recommendation": self.recommendation,
            "recommended_plafond": self.recommended_plafond,
            "created_at": self.created_at,
        }
