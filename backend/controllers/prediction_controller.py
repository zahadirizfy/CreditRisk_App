from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.db import db

from models.prediction import Prediction
from models.result import Result

from ml.predict_model import predict_risk_hybrid


# ==========================================
# CREATE PREDICTION + AI
# ==========================================
@jwt_required()
def create_prediction():

    try:
        data = request.get_json()

        # ==========================
        # IDENTITAS NASABAH
        # ==========================

        name = data.get("name")
        id_card = data.get("id_card")
        work = data.get("work")

        if not data:
            return jsonify({"success": False, "message": "Data tidak ditemukan"}), 400

        if not name:
            return jsonify(
                {"success": False, "message": "Nama nasabah wajib diisi"}
            ), 400

        if not id_card:
            return jsonify({"success": False, "message": "Nomor KTP wajib diisi"}), 400

        if not work:
            return jsonify(
                {"success": False, "message": "Pekerjaan wajib dipilih"}
            ), 400

        user_id = int(get_jwt_identity())

        prediction = Prediction(
            id_user=user_id,
            name=name,
            id_card=id_card,
            work=work,
            revolving_utilization=data.get("revolving_utilization"),
            age=data.get("age"),
            delinquency_30_59=data.get("delinquency_30_59"),
            debt_ratio=data.get("debt_ratio"),
            monthly_income=data.get("monthly_income"),
            number_credit=data.get("number_credit"),
            delinquency_90=data.get("delinquency_90"),
            real_estate_loans=data.get("real_estate_loans"),
            delinquency_60_89=data.get("delinquency_60_89"),
            dependents=data.get("dependents"),
        )

        db.session.add(prediction)

        db.session.flush()

        nasabah = {
            "revolving_utilization": prediction.revolving_utilization,
            "age": prediction.age,
            "delinquency_30_59": prediction.delinquency_30_59,
            "debt_ratio": prediction.debt_ratio,
            "monthly_income": prediction.monthly_income,
            "num_credit_lines": prediction.number_credit,
            "delinquency_90": prediction.delinquency_90,
            "delinquency_60_89": prediction.delinquency_60_89,
            "dependents": prediction.dependents,
            "real_estate_loans": prediction.real_estate_loans,
        }

        hasil = predict_risk_hybrid(nasabah)

        if not hasil["success"]:
            raise Exception(hasil["message"])

        result = Result(
            id_prediction=prediction.id_prediction,
            logistic_probability=hasil["probability"],
            credit_eligibility=hasil["status"],
            knn_k_value=hasil["knn_k_value"],
            risk_level=hasil["risk_level"],
        )

        db.session.add(result)

        db.session.commit()

        return jsonify(
            {
                "success": True,
                "message": "Prediksi berhasil",
                "prediction": {
                    "name": prediction.name,
                    "id_card": prediction.id_card,
                    "work": prediction.work,
                },
                "prediction_id": prediction.id_prediction,
                "result": {
                    "status": hasil["status"],
                    "probability": hasil["probability"],
                    "risk_level": hasil["risk_level"],
                    "risk_code": hasil["risk_code"],
                    "recommended_plafond": hasil.get("recommended_plafond"),
                    "recommendation": hasil.get("recommendation"),
                    "color": hasil.get("color"),
                },
            }
        ), 201

    except Exception as e:
        db.session.rollback()

        return jsonify({"success": False, "message": str(e)}), 500


# ==========================================
# GET ALL PREDICTIONS
# ==========================================
@jwt_required()
def get_predictions():

    try:
        user_id = int(get_jwt_identity())

        predictions = (
            Prediction.query.filter_by(id_user=user_id)
            .order_by(Prediction.prediction_date.desc())
            .all()
        )

        return jsonify(
            {
                "success": True,
                "total_data": len(predictions),
                "data": [prediction.to_dict() for prediction in predictions],
            }
        ), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ==========================================
# GET PREDICTION BY ID
# ==========================================
@jwt_required()
def get_prediction_by_id(id_prediction):

    try:
        prediction = db.session.get(Prediction, id_prediction)

        if not prediction:
            return jsonify(
                {"success": False, "message": "Data prediction tidak ditemukan"}
            ), 404

        return jsonify({"success": True, "data": prediction.to_dict()}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ==========================================
# DELETE PREDICTION
# ==========================================
@jwt_required()
def delete_prediction(id_prediction):

    try:
        prediction = db.session.get(Prediction, id_prediction)

        if not prediction:
            return jsonify(
                {"success": False, "message": "Data prediction tidak ditemukan"}
            ), 404

        db.session.delete(prediction)

        db.session.commit()

        return jsonify(
            {"success": True, "message": "Data prediction berhasil dihapus"}
        ), 200

    except Exception as e:
        db.session.rollback()

        return jsonify({"success": False, "message": str(e)}), 500


# ==========================================
# GET ALL RESULTS
# ==========================================
@jwt_required()
def get_results():

    try:
        results = Result.query.order_by(Result.id_result.desc()).all()

        data = [result.to_dict() for result in results]

        return jsonify({"success": True, "total_data": len(data), "data": data}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
