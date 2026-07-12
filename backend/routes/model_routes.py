from flask import Blueprint

from controllers.model_controller import (
    retrain_model_controller,
    retrain_status_controller,
)

model_bp = Blueprint("model", __name__)


@model_bp.route("/retrain", methods=["POST"])
def retrain_route():
    return retrain_model_controller()


@model_bp.route("/retrain-status", methods=["GET"])
def retrain_status_route():
    return retrain_status_controller()
