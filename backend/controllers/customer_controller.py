from flask import request, jsonify
from flask_jwt_extended import jwt_required

from database.db import db
from decorators.role_required import role_required

from services.customer_service import (
    get_customers_service,
    get_customer_by_id_service,
    create_customer_service,
    update_customer_service,
    delete_customer_service,
    update_customer_status_service,
    get_customer_dashboard_service,
)


# =====================================================
# GET CUSTOMER
# =====================================================


@jwt_required()
@role_required("operator", "super_admin")
def get_customers():

    try:
        page = request.args.get("page", 1, type=int)

        per_page = request.args.get("per_page", 10, type=int)

        search = request.args.get("search", "", type=str)

        data = get_customers_service(
            page=page,
            per_page=per_page,
            search=search,
        )

        return jsonify(
            {
                "success": True,
                "message": "Data berhasil dimuat.",
                "data": data,
            }
        ), 200

    except Exception as e:
        return jsonify(
            {
                "success": False,
                "message": str(e),
            }
        ), 500


# =====================================================
# GET CUSTOMER BY ID
# =====================================================


@jwt_required()
@role_required("operator", "super_admin")
def get_customer_by_id(id_user):

    try:
        data = get_customer_by_id_service(id_user)

        return jsonify(
            {
                "success": True,
                "data": data,
            }
        ), 200

    except Exception as e:
        return jsonify(
            {
                "success": False,
                "message": str(e),
            }
        ), 404


# =====================================================
# CREATE CUSTOMER
# =====================================================


@jwt_required()
@role_required("operator", "super_admin")
def create_customer():

    try:
        data = request.get_json()

        customer = create_customer_service(data)

        return jsonify(
            {
                "success": True,
                "message": "Data berhasil ditambahkan.",
                "data": customer,
            }
        ), 201

    except Exception as e:
        db.session.rollback()

        return jsonify(
            {
                "success": False,
                "message": str(e),
            }
        ), 400


# =====================================================
# UPDATE CUSTOMER
# =====================================================


@jwt_required()
@role_required("operator", "super_admin")
def update_customer(id_user):

    try:
        data = request.get_json()

        customer = update_customer_service(
            id_user,
            data,
        )

        return jsonify(
            {
                "success": True,
                "message": "Data berhasil diperbarui.",
                "data": customer,
            }
        ), 200

    except Exception as e:
        db.session.rollback()

        return jsonify(
            {
                "success": False,
                "message": str(e),
            }
        ), 400


# =====================================================
# DELETE CUSTOMER
# =====================================================


@jwt_required()
@role_required("operator", "super_admin")
def delete_customer(id_user):

    try:
        delete_customer_service(id_user)

        return jsonify(
            {
                "success": True,
                "message": "Data berhasil dihapus.",
            }
        ), 200

    except Exception as e:
        db.session.rollback()

        return jsonify(
            {
                "success": False,
                "message": str(e),
            }
        ), 400


# =====================================================
# UPDATE STATUS CUSTOMER
# =====================================================


@jwt_required()
@role_required("operator")
def update_customer_status(id_user):

    try:
        data = request.get_json()

        customer = update_customer_status_service(id_user, data.get("status_aktif"))

        return jsonify(
            {
                "success": True,
                "message": "Status berhasil diperbarui.",
                "data": customer,
            }
        ), 200

    except Exception as e:
        db.session.rollback()

        return jsonify({"success": False, "message": str(e)}), 400


# =====================================================
# CUSTOMER DASHBOARD
# =====================================================


@jwt_required()
@role_required("operator", "super_admin")
def get_customer_dashboard():

    try:
        data = get_customer_dashboard_service()

        return jsonify(
            {
                "success": True,
                "message": "Dashboard berhasil dimuat.",
                "data": data,
            }
        ), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
