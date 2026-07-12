from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.db import db

from models.prediction import Prediction
from models.result import Result

from ml.predict_model import THRESHOLD, predict_risk_hybrid
from decorators.role_required import role_required


# ==========================================
# CREATE PREDICTION + AI
# ==========================================
@jwt_required()
@role_required("instansi", "nasabah")
def create_prediction():

    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "message": "Data tidak ditemukan."}), 400

        # ==========================================
        # IDENTITAS NASABAH
        # ==========================================

        name = data.get("name")
        id_card = data.get("id_card")
        work = data.get("work")

        if not name:
            return jsonify(
                {"success": False, "message": "Nama nasabah wajib diisi."}
            ), 400

        if not id_card:
            return jsonify({"success": False, "message": "Nomor KTP wajib diisi."}), 400

        if not work:
            return jsonify(
                {"success": False, "message": "Pekerjaan wajib dipilih."}
            ), 400

        # ==========================================
        # VALIDASI DATA NUMERIK
        # ==========================================

        try:
            revolving_utilization = float(data.get("revolving_utilization"))
            age = int(data.get("age"))
            debt_ratio = float(data.get("debt_ratio"))
            monthly_income = float(data.get("monthly_income"))
            number_credit = int(data.get("number_credit"))
            delinquency_30_59 = int(data.get("delinquency_30_59"))
            delinquency_60_89 = int(data.get("delinquency_60_89"))
            delinquency_90 = int(data.get("delinquency_90"))
            real_estate_loans = int(data.get("real_estate_loans"))
            dependents = int(data.get("dependents"))

        except (TypeError, ValueError):
            return jsonify(
                {"success": False, "message": "Format data numerik tidak valid."}
            ), 400

        # ==========================================
        # VALIDASI NILAI
        # ==========================================

        if age <= 0:
            return jsonify(
                {"success": False, "message": "Usia harus lebih dari 0."}
            ), 400

        if revolving_utilization < 0:
            return jsonify(
                {
                    "success": False,
                    "message": "Revolving utilization tidak boleh negatif.",
                }
            ), 400

        if debt_ratio < 0:
            return jsonify(
                {"success": False, "message": "Debt ratio tidak boleh negatif."}
            ), 400

        if monthly_income < 0:
            return jsonify(
                {"success": False, "message": "Pendapatan tidak boleh negatif."}
            ), 400

        if number_credit < 0:
            return jsonify(
                {"success": False, "message": "Jumlah kredit tidak boleh negatif."}
            ), 400

        if delinquency_30_59 < 0 or delinquency_60_89 < 0 or delinquency_90 < 0:
            return jsonify(
                {
                    "success": False,
                    "message": "Jumlah keterlambatan tidak boleh negatif.",
                }
            ), 400

        if real_estate_loans < 0:
            return jsonify(
                {
                    "success": False,
                    "message": "Jumlah pinjaman properti tidak boleh negatif.",
                }
            ), 400

        if dependents < 0:
            return jsonify(
                {"success": False, "message": "Jumlah tanggungan tidak boleh negatif."}
            ), 400

        # ==========================================
        # SIMPAN DATA PREDIKSI
        # ==========================================

        user_id = int(get_jwt_identity())

        prediction = Prediction(
            id_user=user_id,
            name=name,
            id_card=id_card,
            work=work,
            revolving_utilization=revolving_utilization,
            age=age,
            delinquency_30_59=delinquency_30_59,
            debt_ratio=debt_ratio,
            monthly_income=monthly_income,
            number_credit=number_credit,
            delinquency_90=delinquency_90,
            real_estate_loans=real_estate_loans,
            delinquency_60_89=delinquency_60_89,
            dependents=dependents,
        )

        db.session.add(prediction)
        db.session.flush()

        # ==========================================
        # MACHINE LEARNING
        # ==========================================

        nasabah = {
            "revolving_utilization": revolving_utilization,
            "age": age,
            "delinquency_30_59": delinquency_30_59,
            "debt_ratio": debt_ratio,
            "monthly_income": monthly_income,
            "num_credit_lines": number_credit,
            "delinquency_90": delinquency_90,
            "real_estate_loans": real_estate_loans,
            "delinquency_60_89": delinquency_60_89,
            "dependents": dependents,
        }

        hasil = predict_risk_hybrid(nasabah)

        if not hasil["success"]:
            db.session.rollback()

            return jsonify(
                {"success": False, "message": hasil.get("message", "Prediksi gagal.")}
            ), 400

        # ==========================================
        # SIMPAN HASIL MODEL
        # ==========================================

        result = Result(
            id_prediction=prediction.id_prediction,
            logistic_probability=hasil["probability"],
            credit_eligibility=hasil["status"],
            risk_probability=hasil["risk_probability"],
            risk_level=hasil["risk_level"],
            knn_k_value=hasil["knn_k_value"],
            recommendation=hasil["recommendation"],
            recommended_plafond=hasil["recommended_plafond"],
        )

        db.session.add(result)

        db.session.commit()

        # ==========================================
        # RESPONSE
        # ==========================================

        return jsonify(
            {
                "success": True,
                "message": "Prediksi berhasil.",
                "prediction": {
                    "id_prediction": prediction.id_prediction,
                    "prediction_date": prediction.prediction_date,
                    "name": prediction.name,
                    "id_card": prediction.id_card,
                    "work": prediction.work,
                },
                "result": {
                    "status": hasil["status"],
                    "probability": hasil["probability"],
                    "threshold": THRESHOLD,
                    "risk_probability": hasil["risk_probability"],
                    "risk_level": hasil["risk_level"],
                    "risk_code": hasil["risk_code"],
                    "recommended_plafond": hasil["recommended_plafond"],
                    "recommendation": hasil["recommendation"],
                    "color": hasil["color"],
                    "knn_k_value": hasil["knn_k_value"],
                },
            }
        ), 201

    except Exception:
        db.session.rollback()

        return jsonify(
            {"success": False, "message": "Terjadi kesalahan pada server."}
        ), 500


# ==========================================
# GET ALL PREDICTIONS
# ==========================================
@jwt_required()
@role_required("instansi", "nasabah")
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

    except Exception:
        return jsonify(
            {"success": False, "message": "Terjadi kesalahan pada server."}
        ), 500


# ==========================================
# GET PREDICTION BY ID
# ==========================================
@jwt_required()
@role_required("instansi", "nasabah")
def get_prediction_by_id(id_prediction):

    try:
        user_id = int(get_jwt_identity())

        prediction = Prediction.query.filter_by(
            id_prediction=id_prediction, id_user=user_id
        ).first()

        if not prediction:
            return jsonify(
                {"success": False, "message": "Data prediction tidak ditemukan."}
            ), 404

        return jsonify({"success": True, "data": prediction.to_dict()}), 200

    except Exception:
        return jsonify(
            {"success": False, "message": "Terjadi kesalahan pada server."}
        ), 500


# ==========================================
# DELETE PREDICTION
# ==========================================
@jwt_required()
@role_required("instansi", "nasabah")
def delete_prediction(id_prediction):

    try:
        user_id = int(get_jwt_identity())

        prediction = Prediction.query.filter_by(
            id_prediction=id_prediction, id_user=user_id
        ).first()

        if not prediction:
            return jsonify(
                {"success": False, "message": "Data prediction tidak ditemukan."}
            ), 404

        db.session.delete(prediction)

        db.session.commit()

        return jsonify(
            {"success": True, "message": "Data prediction berhasil dihapus."}
        ), 200

    except Exception:
        db.session.rollback()

        return jsonify(
            {"success": False, "message": "Terjadi kesalahan pada server."}
        ), 500


# ==========================================
# GET ALL RESULTS
# ==========================================
@jwt_required()
@role_required("super_admin")
def get_results():

    try:
        results = Result.query.order_by(Result.id_result.desc()).all()

        return jsonify(
            {
                "success": True,
                "total_data": len(results),
                "data": [result.to_dict() for result in results],
            }
        ), 200

    except Exception:
        return jsonify(
            {"success": False, "message": "Terjadi kesalahan pada server."}
        ), 500
