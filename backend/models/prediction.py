from database.db import db
from datetime import datetime


class Prediction(db.Model):
    __tablename__ = "predictions"

    result = db.relationship(
        "Result", backref="prediction", uselist=False, cascade="all, delete-orphan"
    )

    id_prediction = db.Column(db.Integer, primary_key=True)

    id_user = db.Column(db.Integer, db.ForeignKey("users.id_user"), nullable=False)

    name = db.Column(db.String(50), nullable=False)

    id_card = db.Column(db.String(20), nullable=False, unique=False)

    work = db.Column(db.String(50), nullable=False)

    revolving_utilization = db.Column(db.Float)

    age = db.Column(db.Integer)

    delinquency_30_59 = db.Column(db.Integer)

    debt_ratio = db.Column(db.Float)

    monthly_income = db.Column(db.Float)

    number_credit = db.Column(db.Integer)

    delinquency_90 = db.Column(db.Integer)

    real_estate_loans = db.Column(db.Integer)

    delinquency_60_89 = db.Column(db.Integer)

    dependents = db.Column(db.Integer)

    prediction_date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id_prediction": self.id_prediction,
            "id_user": self.id_user,
            "name": self.name,
            "id_card": self.id_card,
            "work": self.work,
            "revolving_utilization": self.revolving_utilization,
            "age": self.age,
            "delinquency_30_59": self.delinquency_30_59,
            "debt_ratio": self.debt_ratio,
            "monthly_income": self.monthly_income,
            "number_credit": self.number_credit,
            "delinquency_90": self.delinquency_90,
            "real_estate_loans": self.real_estate_loans,
            "delinquency_60_89": self.delinquency_60_89,
            "dependents": self.dependents,
            "prediction_date": self.prediction_date,
            "result": (self.result.to_dict() if self.result else None),
        }
