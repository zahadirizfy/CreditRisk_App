from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity

from models.user import User


def role_required(*allowed_roles):
    """
    Decorator untuk membatasi akses berdasarkan role.
    Contoh:
        @jwt_required()
        @role_required("super_admin")

        @jwt_required()
        @role_required("super_admin", "operator")
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            user_id = int(get_jwt_identity())

            user = User.query.get(user_id)

            if not user:
                return jsonify({
                    "success": False,
                    "message": "User tidak ditemukan."
                }), 404

            if not user.status_aktif:
                return jsonify({
                    "success": False,
                    "message": "Akun telah dinonaktifkan."
                }), 403

            if user.role not in allowed_roles:
                return jsonify({
                    "success": False,
                    "message": "Anda tidak memiliki hak akses."
                }), 403

            return func(*args, **kwargs)

        return wrapper

    return decorator