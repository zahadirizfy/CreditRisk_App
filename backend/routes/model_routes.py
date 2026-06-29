from flask import Blueprint
from controllers.model_controller import train_model

model_bp = Blueprint(
    "model",
    __name__
)

@model_bp.route(
    "/model/train",
    methods=["POST"]
)
def train_model_route():
    return train_model()