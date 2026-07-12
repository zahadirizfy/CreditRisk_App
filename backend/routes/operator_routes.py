from flask import Blueprint

from controllers.operator_controller import (
    delete_operator,
    get_operators,
    create_operator,
    update_operator,
    update_operator_status,
    delete_operator_service,
)

# =====================================================
# BLUEPRINT
# =====================================================

operator_bp = Blueprint(
    "operator",
    __name__,
)

# =====================================================
# OPERATOR
# =====================================================


@operator_bp.route(
    "/operators",
    methods=["GET"],
)
def get_operator_route():
    return get_operators()


@operator_bp.route(
    "/operators",
    methods=["POST"],
)
def create_operator_route():
    return create_operator()


@operator_bp.route("/operators/<int:id_user>", methods=["PUT"])
def update_operator_route(id_user):

    return update_operator(id_user)


@operator_bp.route("/operators/<int:id_user>/status", methods=["PATCH"])
def update_operator_status_route(id_user):

    return update_operator_status(id_user)


@operator_bp.route("/operators/<int:id_user>", methods=["DELETE"])
def delete_operator_route(id_user):

    return delete_operator(id_user)
    