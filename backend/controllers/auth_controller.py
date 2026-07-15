import random
from flask import request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta

from database.db import db
from models.user import User
from sqlalchemy import or_
from decorators.role_required import role_required
from utils.email_sender import send_reset_email


# ==========================================
# REGISTER
# =========================================
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
        instansi = data.get("instansi")
        role = data.get("role")

        if not username:
            return jsonify({"success": False, "message": "Username wajib diisi"}), 400

        if not email:
            return jsonify({"success": False, "message": "Email wajib diisi"}), 400

        if not password:
            return jsonify({"success": False, "message": "Password wajib diisi"}), 400

        if not nomor_telepon:
            return jsonify(
                {"success": False, "message": "Nomor telepon wajib diisi"}
            ), 400

        allowed_roles = ["nasabah", "instansi"]

        if role not in allowed_roles:
            return jsonify({"success": False, "message": "Role tidak valid"}), 400

        if role == "instansi" and not instansi:
            return jsonify(
                {
                    "success": False,
                    "message": "Nama instansi wajib diisi",
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

        if nomor_telepon:
            existing_phone = User.query.filter_by(nomor_telepon=nomor_telepon).first()

        if existing_phone:
            return jsonify(
                {"success": False, "message": "Nomor telepon sudah digunakan."}
            ), 409

        hashed_password = generate_password_hash(password).decode("utf-8")

        new_user = User(
            username=username,
            password=hashed_password,
            nama_lengkap=nama_lengkap,
            email=email,
            nomor_telepon=nomor_telepon,
            instansi=instansi,
            role=role,
            status_aktif=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
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
                    "nomor_telepon": new_user.nomor_telepon,
                    "role": new_user.role,
                },
            }
        ), 201

    except Exception:
        db.session.rollback()

        return jsonify(
            {"success": False, "message": "Terjadi kesalahan pada server."}
        ), 500


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

        user.terakhir_login = datetime.utcnow()
        user.updated_at = datetime.utcnow()

        db.session.commit()

        return jsonify(
            {
                "success": True,
                "message": "Login berhasil",
                "access_token": access_token,
                "user": {
                    "id_user": user.id_user,
                    "username": user.username,
                    "nama_lengkap": user.nama_lengkap,
                    "email": user.email,
                    "nomor_telepon": user.nomor_telepon,
                    "instansi": user.instansi,
                    "role": user.role,
                    "status_aktif": user.status_aktif,
                },
            }
        ), 200

    except Exception:
        db.session.rollback()

        return jsonify(
            {"success": False, "message": "Terjadi kesalahan pada server"}
        ), 500


# ==========================================
# 1. MINTA KODE RESET (LUPA PASSWORD)
# ==========================================
def forgot_password():
    try:
        data = request.get_json()
        email = data.get("email")

        if not email:
            return jsonify({"success": False, "message": "Email wajib diisi"}), 400

        user = User.query.filter_by(email=email).first()

        if not user:
            # Tetap berikan respon 404 agar user tahu emailnya tidak terdaftar
            return jsonify(
                {"success": False, "message": "Email tidak terdaftar di sistem kami."}
            ), 404

        # Generate 6 digit OTP acak
        otp_code = str(random.randint(100000, 999999))

        # Simpan OTP dan waktu kadaluarsa (15 menit dari sekarang) ke database
        user.reset_code = otp_code
        user.reset_code_expired_at = datetime.utcnow() + timedelta(minutes=15)
        db.session.commit()

        # Kirim email
        email_sent = send_reset_email(user.email, otp_code)

        if email_sent:
            return jsonify(
                {"success": True, "message": "Kode OTP telah dikirim ke email Anda."}
            ), 200
        else:
            return jsonify(
                {"success": False, "message": "Gagal mengirim email. Coba lagi nanti."}
            ), 500

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500


# ==========================================
# 2. VERIFIKASI KODE & RESET PASSWORD
# ==========================================
def reset_password():
    try:
        data = request.get_json()
        email = data.get("email")
        otp_code = data.get("otp_code")
        new_password = data.get("new_password")

        if not email or not otp_code or not new_password:
            return jsonify(
                {
                    "success": False,
                    "message": "Email, kode OTP, dan password baru wajib diisi",
                }
            ), 400

        user = User.query.filter_by(email=email).first()

        # Validasi eksistensi user dan kecocokan OTP
        if not user or user.reset_code != otp_code:
            return jsonify(
                {"success": False, "message": "Kode OTP salah atau tidak valid."}
            ), 400

        # Validasi waktu kadaluarsa OTP
        if (
            not user.reset_code_expired_at
            or user.reset_code_expired_at < datetime.utcnow()
        ):
            return jsonify(
                {
                    "success": False,
                    "message": "Kode OTP sudah kadaluarsa. Silakan minta kode baru.",
                }
            ), 400

        # Jika lolos semua validasi, Hash password baru
        hashed_password = generate_password_hash(new_password).decode("utf-8")
        user.password = hashed_password

        # Bersihkan kolom OTP agar tidak bisa dipakai ulang
        user.reset_code = None
        user.reset_code_expired_at = None
        user.updated_at = datetime.utcnow()

        db.session.commit()

        return jsonify(
            {
                "success": True,
                "message": "Password berhasil direset. Silakan login dengan password baru.",
            }
        ), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500


# ==========================================
# PROFILE
# ==========================================
@jwt_required()
def profile():

    try:
        user_id = int(get_jwt_identity())

        user = db.session.get(User, user_id)

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

        user = db.session.get(User, user_id)

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

        nomor_telepon = data.get(
            "nomor_telepon",
            user.nomor_telepon,
        )

        if nomor_telepon:
            existing_phone = User.query.filter(
                User.nomor_telepon == nomor_telepon,
                User.id_user != user.id_user,
            ).first()

        if existing_phone:
            return jsonify(
                {"success": False, "message": "Nomor telepon sudah digunakan."}
            ), 409

        user.nama_lengkap = data.get("nama_lengkap", user.nama_lengkap)

        user.username = username

        user.email = email

        user.nomor_telepon = nomor_telepon

        # Hanya selain nasabah yang boleh mengubah instansi
        if user.role != "nasabah":
            user.instansi = data.get("instansi", user.instansi)

        user.updated_at = datetime.utcnow()

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

        user = db.session.get(User, user_id)

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
        user.updated_at = datetime.utcnow()

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
@role_required("super_admin", "operator")
def get_users():

    try:
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
@role_required("super_admin", "operator")
def get_user_by_id(id_user):

    try:
        user = db.session.get(User, id_user)

        if not user:
            return jsonify({"success": False, "message": "User tidak ditemukan"}), 404

        return jsonify({"success": True, "data": user.to_dict()}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
