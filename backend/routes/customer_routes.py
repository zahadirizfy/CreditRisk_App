from flask import Blueprint

from controllers.customer_controller import (
    get_customers,
    get_customer_by_id,
    create_customer,
    update_customer,
    delete_customer,
    update_customer_status,
    get_customer_dashboard,
)

customer_bp = Blueprint("customer", __name__)


# =====================================================
# CUSTOMER
# =====================================================


@customer_bp.route("/customers/dashboard", methods=["GET"])
def get_customer_dashboard_route():

    return get_customer_dashboard()


@customer_bp.route("/customers", methods=["GET"])
def get_customers_route():

    return get_customers()


@customer_bp.route("/customers/<int:id_user>", methods=["GET"])
def get_customer_by_id_route(id_user):

    return get_customer_by_id(id_user)


@customer_bp.route("/customers", methods=["POST"])
def create_customer_route():

    return create_customer()


@customer_bp.route("/customers/<int:id_user>", methods=["PUT"])
def update_customer_route(id_user):

    return update_customer(id_user)


@customer_bp.route("/customers/<int:id_user>", methods=["DELETE"])
def delete_customer_route(id_user):

    return delete_customer(id_user)


@customer_bp.route("/customers/<int:id_user>/status", methods=["PATCH"])
def update_customer_status_route(id_user):
    return update_customer_status(id_user)
