from flask import jsonify, request
from flask_jwt_extended import jwt_required
from database.db import db
from decorators.role_required import role_required
from services.operator_service import (
    get_operator_service,
    create_operator_service,
    update_operator_service,
    update_operator_status_service,
    delete_operator_service,
)
from flask import request


# =====================================================
# GET OPERATOR
# =====================================================


@jwt_required()
@role_required("super_admin")
def get_operators():

    try:
        page = request.args.get(
            "page",
            default=1,
            type=int,
        )

        per_page = request.args.get(
            "per_page",
            default=10,
            type=int,
        )

        search = request.args.get(
            "search",
            default="",
            type=str,
        )

        data = get_operator_service(
            page=page,
            per_page=per_page,
            search=search,
        )

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Data operator berhasil diambil.",
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


# =====================================================
# CREATE OPERATOR
# =====================================================


@jwt_required()
@role_required("super_admin")
def create_operator():

    try:
        data = request.get_json()

        operator = create_operator_service(data)

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Operator berhasil ditambahkan.",
                    "data": operator,
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()

        return (jsonify({"success": False, "message": str(e)}), 400)


# =====================================================
# UPDATE OPERATOR
# =====================================================


@jwt_required()
@role_required("super_admin")
def update_operator(id_user):

    try:
        data = request.get_json()

        operator = update_operator_service(id_user, data)

        return jsonify(
            {
                "success": True,
                "message": "Operator berhasil diperbarui.",
                "data": operator,
            }
        ), 200

    except Exception as e:
        db.session.rollback()

        return jsonify({"success": False, "message": str(e)}), 400


# =====================================================
# UPDATE STATUS
# =====================================================


@jwt_required()
@role_required("super_admin")
def update_operator_status(id_user):

    try:
        data = request.get_json()

        operator = update_operator_status_service(id_user, data.get("status_aktif"))

        return jsonify(
            {
                "success": True,
                "message": "Status operator berhasil diperbarui.",
                "data": operator,
            }
        ), 200

    except Exception as e:
        db.session.rollback()

        return jsonify({"success": False, "message": str(e)}), 400


# =====================================================
# DELETE OPERATOR
# =====================================================


@jwt_required()
@role_required("super_admin")
def delete_operator(id_user):

    try:
        delete_operator_service(id_user)

        return jsonify({"success": True, "message": "Operator berhasil dihapus."}), 200

    except Exception as e:
        db.session.rollback()

        return jsonify({"success": False, "message": str(e)}), 400
