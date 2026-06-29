from flask import Blueprint

from controllers.prediction_controller import (
    create_prediction,
    get_predictions,
    get_prediction_by_id,
    delete_prediction,
    get_results
)

prediction_bp = Blueprint(
    "prediction",
    __name__
)


# ==========================================
# AI PREDICTION
# ==========================================

@prediction_bp.route(
    "/predict",
    methods=["POST"]
)
def predict_route():
    return create_prediction()


# ==========================================
# PREDICTION HISTORY
# ==========================================

@prediction_bp.route(
    "/predictions",
    methods=["GET"]
)
def get_predictions_route():
    return get_predictions()


@prediction_bp.route(
    "/predictions/<int:id_prediction>",
    methods=["GET"]
)
def get_prediction_by_id_route(id_prediction):
    return get_prediction_by_id(id_prediction)


@prediction_bp.route(
    "/predictions/<int:id_prediction>",
    methods=["DELETE"]
)
def delete_prediction_route(id_prediction):
    return delete_prediction(id_prediction)


# ==========================================
# RESULTS
# ==========================================

@prediction_bp.route(
    "/results",
    methods=["GET"]
)
def get_results_route():
    return get_results()