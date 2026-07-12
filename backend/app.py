from flask import Flask
from flask_cors import CORS

from config import Config
from database.db import db

from flask_jwt_extended import JWTManager

from routes.auth_routes import auth_bp
from routes.prediction_routes import prediction_bp
from routes.model_routes import model_bp
from routes.dashboard_routes import dashboard_bp
from routes.operator_routes import operator_bp
from routes.customer_routes import customer_bp


app = Flask(__name__)

CORS(app)
# Configuration
app.config.from_object(Config)

# Extensions
db.init_app(app)
jwt = JWTManager(app)

# Blueprints
app.register_blueprint(auth_bp, url_prefix="/api")

app.register_blueprint(prediction_bp, url_prefix="/api")

app.register_blueprint(model_bp, url_prefix="/api")


# Home
@app.route("/")
def home():

    return {"success": True, "message": "Backend Credit Risk API Running"}


app.register_blueprint(
    dashboard_bp,
    url_prefix="/api",
)

app.register_blueprint(
    operator_bp,
    url_prefix="/api",
)

app.register_blueprint(
    customer_bp,
    url_prefix="/api",
)

if __name__ == "__main__":
    app.run(debug=True)
