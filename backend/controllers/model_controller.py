from flask import jsonify, request
from flask_jwt_extended import jwt_required

from decorators.role_required import role_required
from services.model_service import retrain_service

from utils.retrain_status import get_status


# ==========================================
# RETRAIN MODEL
# ==========================================


@jwt_required()
@role_required("super_admin")
def retrain_model_controller():

    print(">>> MASUK CONTROLLER RETRAIN <<<")

    try:
        file = request.files.get("dataset")

        result = retrain_service(file)

        status_code = 200 if result["success"] else 400

        return jsonify(result), status_code

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# =====================================================
# GET RETRAIN STATUS
# =====================================================


def retrain_status_controller():
    try:
        status = get_status()

        return (
            jsonify(
                {
                    "success": True,
                    "data": status,
                }
            ),
            200,
        )

    except Exception as e:
        return (
            jsonify(
                {
                    "success": False,
                    "message": str(e),
                }
            ),
            500,
        )
