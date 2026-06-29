from database.db import db
from datetime import datetime


class Result(db.Model):
    __tablename__ = "results"

    id_result = db.Column(db.Integer, primary_key=True)

    id_prediction = db.Column(
        db.Integer, db.ForeignKey("predictions.id_prediction"), nullable=False
    )

    logistic_probability = db.Column(db.Float)

    credit_eligibility = db.Column(db.String(20))

    knn_k_value = db.Column(db.Integer)

    risk_level = db.Column(db.String(20))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id_result": self.id_result,
            "id_prediction": self.id_prediction,
            "logistic_probability": self.logistic_probability,
            "credit_eligibility": self.credit_eligibility,
            "knn_k_value": self.knn_k_value,
            "risk_level": self.risk_level,
            "created_at": self.created_at,
        }
