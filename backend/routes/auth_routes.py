from flask import Blueprint

from controllers.auth_controller import (
    register,
    login,
    profile,
    update_profile,
    change_password,
    get_users,
    get_user_by_id,
)

auth_bp = Blueprint("auth", __name__)


# ==========================================
# AUTH
# ==========================================


@auth_bp.route("/register", methods=["POST"])
def register_route():
    return register()


@auth_bp.route("/login", methods=["POST"])
def login_route():
    return login()


@auth_bp.route("/profile", methods=["GET"])
def profile_route():
    return profile()


@auth_bp.route("/profile", methods=["PUT"])
def update_profile_route():
    return update_profile()


@auth_bp.route("/profile/change-password", methods=["PUT"])
def change_password_route():
    return change_password()


# ==========================================
# USERS
# ==========================================


@auth_bp.route("/users", methods=["GET"])
def get_users_route():
    return get_users()


@auth_bp.route("/users/<int:id_user>", methods=["GET"])
def get_user_by_id_route(id_user):
    return get_user_by_id(id_user)
