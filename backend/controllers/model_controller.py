from flask import jsonify
from ml.train_model import train_hybrid_model_v2


def train_model():

    try:
        result = train_hybrid_model_v2()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
