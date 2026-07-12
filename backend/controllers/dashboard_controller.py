from flask import jsonify
from flask_jwt_extended import jwt_required

from decorators.role_required import role_required
from services.dashboard_service import dashboard_service


# =====================================================
# DASHBOARD
# =====================================================

@jwt_required()
@role_required("super_admin")
def dashboard_controller():
    """
    Mengambil seluruh data dashboard administrator.
    """

    try:

        data = dashboard_service()

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Dashboard berhasil dimuat.",
                    "data": data,
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