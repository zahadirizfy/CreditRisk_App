from flask import request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime

from database.db import db
from models.user import User
from sqlalchemy import or_


# ==========================================
# REGISTER
# ==========================================
def register():

    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "message": "Data tidak ditemukan"}), 400

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        nama_lengkap = data.get("nama_lengkap")
        nomor_telepon = data.get("nomor_telepon")
        institusi = data.get("institusi")
        role = data.get("role")

        if not username:
            return jsonify({"success": False, "message": "Username wajib diisi"}), 400

        if not email:
            return jsonify({"success": False, "message": "Email wajib diisi"}), 400

        if not password:
            return jsonify({"success": False, "message": "Password wajib diisi"}), 400

        allowed_roles = ["nasabah", "admin_bank"]

        if role not in allowed_roles:
            return jsonify({"success": False, "message": "Role tidak valid"}), 400

        if role == "admin_bank" and not institusi:
            return jsonify(
                {
                    "success": False,
                    "message": "Institusi wajib diisi untuk Admin Bank/Koperasi",
                }
            ), 400

        existing_username = User.query.filter_by(username=username).first()

        if existing_username:
            return jsonify(
                {"success": False, "message": "Username sudah digunakan"}
            ), 409

        existing_email = User.query.filter_by(email=email).first()

        if existing_email:
            return jsonify({"success": False, "message": "Email sudah digunakan"}), 409

        hashed_password = generate_password_hash(password).decode("utf-8")

        new_user = User(
            username=username,
            password=hashed_password,
            nama_lengkap=nama_lengkap,
            email=email,
            nomor_telepon=nomor_telepon,
            institusi=institusi,
            role=role,
            status_aktif=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify(
            {
                "success": True,
                "message": "Registrasi berhasil",
                "data": {
                    "id_user": new_user.id_user,
                    "username": new_user.username,
                    "email": new_user.email,
                    "role": new_user.role,
                },
            }
        ), 201

    except Exception as e:
        db.session.rollback()

        return jsonify({"success": False, "message": str(e)}), 500


# ==========================================
# LOGIN
# ==========================================
def login():

    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "message": "Data tidak ditemukan"}), 400

        login_input = data.get("login_input")
        password = data.get("password")

        if not login_input or not password:
            return jsonify(
                {
                    "success": False,
                    "message": "Username/Email/No Telepon dan Password wajib diisi",
                }
            ), 400

        user = User.query.filter(
            or_(
                User.username == login_input,
                User.email == login_input,
                User.nomor_telepon == login_input,
            )
        ).first()

        # Security:
        # Jangan beri tahu apakah user atau password yang salah

        if not user or not check_password_hash(user.password, password):
            return jsonify(
                {
                    "success": False,
                    "message": "Username/Email/No Telepon atau Password salah",
                }
            ), 401

        if not user.status_aktif:
            return jsonify(
                {
                    "success": False,
                    "message": "Akun tidak aktif. Silakan hubungi administrator.",
                }
            ), 403

        access_token = create_access_token(identity=str(user.id_user))

        user.terakhir_login = datetime.now()
        user.updated_at = datetime.now()

        db.session.commit()

        return jsonify(
            {
                "success": True,
                "message": "Login berhasil",
                "token": access_token,
                "user": {
                    "id_user": user.id_user,
                    "username": user.username,
                    "nama_lengkap": user.nama_lengkap,
                    "email": user.email,
                    "role": user.role,
                },
            }
        ), 200

    except Exception as e:
        db.session.rollback()

        return jsonify(
            {"success": False, "message": "Terjadi kesalahan pada server"}
        ), 500


# ==========================================
# PROFILE
# ==========================================
@jwt_required()
def profile():

    try:
        user_id = int(get_jwt_identity())

        user = User.query.get(user_id)

        if not user:
            return jsonify({"success": False, "message": "User tidak ditemukan"}), 404

        return jsonify({"success": True, "data": user.to_dict()}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ==========================================
# UPDATE PROFILE
# ==========================================


@jwt_required()
def update_profile():

    try:
        user_id = int(get_jwt_identity())

        user = User.query.get(user_id)

        if not user:
            return jsonify({"success": False, "message": "User tidak ditemukan"}), 404

        data = request.get_json()

        if not data:
            return jsonify({"success": False, "message": "Data tidak ditemukan"}), 400

        username = data.get("username", user.username)

        email = data.get("email", user.email)

        existing_username = User.query.filter(
            User.username == username, User.id_user != user.id_user
        ).first()

        if existing_username:
            return jsonify(
                {"success": False, "message": "Username sudah digunakan"}
            ), 409

        existing_email = User.query.filter(
            User.email == email, User.id_user != user.id_user
        ).first()

        if existing_email:
            return jsonify({"success": False, "message": "Email sudah digunakan"}), 409

        user.nama_lengkap = data.get("nama_lengkap", user.nama_lengkap)

        user.username = username

        user.email = email

        user.nomor_telepon = data.get("nomor_telepon", user.nomor_telepon)

        # Hanya selain nasabah yang boleh mengubah institusi
        if user.role != "nasabah":
            user.institusi = data.get("institusi", user.institusi)

        user.updated_at = datetime.now()

        db.session.commit()

        return jsonify(
            {
                "success": True,
                "message": "Profil berhasil diperbarui",
                "data": user.to_dict(),
            }
        ), 200

    except Exception as e:
        db.session.rollback()

        return jsonify({"success": False, "message": str(e)}), 500


# ==========================================
# CHANGE PASSWORD
# ==========================================


@jwt_required()
def change_password():

    try:
        user_id = int(get_jwt_identity())

        user = User.query.get(user_id)

        if not user:
            return jsonify({"success": False, "message": "User tidak ditemukan"}), 404

        data = request.get_json()

        if not data:
            return jsonify({"success": False, "message": "Data tidak ditemukan"}), 400

        current_password = data.get("current_password")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")

        if not current_password or not new_password or not confirm_password:
            return jsonify(
                {"success": False, "message": "Semua field wajib diisi"}
            ), 400

        if not check_password_hash(user.password, current_password):
            return jsonify({"success": False, "message": "Password lama salah"}), 400

        if len(new_password) < 8:
            return jsonify(
                {"success": False, "message": "Password minimal 8 karakter"}
            ), 400

        if new_password != confirm_password:
            return jsonify(
                {"success": False, "message": "Konfirmasi password tidak sama"}
            ), 400

        if check_password_hash(user.password, new_password):
            return jsonify(
                {
                    "success": False,
                    "message": "Password baru harus berbeda dari password lama",
                }
            ), 400

        hashed_password = generate_password_hash(new_password).decode("utf-8")

        user.password = hashed_password
        user.updated_at = datetime.now()

        db.session.commit()

        return jsonify(
            {"success": True, "message": "Password berhasil diperbarui"}
        ), 200

    except Exception as e:
        db.session.rollback()

        return jsonify({"success": False, "message": str(e)}), 500


# ==========================================
# GET ALL USERS
# ==========================================
@jwt_required()
def get_users():

    try:
        current_user_id = int(get_jwt_identity())

        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({"success": False, "message": "User tidak ditemukan"}), 404

        if current_user.role != "super_admin":
            return jsonify({"success": False, "message": "Akses ditolak"}), 403

        users = User.query.all()

        return jsonify(
            {
                "success": True,
                "total_data": len(users),
                "data": [user.to_dict() for user in users],
            }
        ), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ==========================================
# GET USER BY ID
# ==========================================
@jwt_required()
def get_user_by_id(id_user):

    try:
        current_user_id = int(get_jwt_identity())

        current_user = User.query.get(current_user_id)

        if not current_user:
            return jsonify({"success": False, "message": "User tidak ditemukan"}), 404

        if current_user.role != "super_admin":
            return jsonify({"success": False, "message": "Akses ditolak"}), 403

        user = User.query.get(id_user)

        if not user:
            return jsonify({"success": False, "message": "User tidak ditemukan"}), 404

        return jsonify({"success": True, "data": user.to_dict()}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
