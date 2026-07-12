from sqlalchemy import or_

from models.user import User

from flask_bcrypt import generate_password_hash
from datetime import datetime
from database.db import db


# =====================================================
# GET OPERATOR
# =====================================================


def get_operator_service(page, per_page, search):

    query = User.query.filter(User.role == "operator")

    if search:
        query = query.filter(
            or_(
                User.nama_lengkap.ilike(f"%{search}%"),
                User.username.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
                User.instansi.ilike(f"%{search}%"),
            )
        )

    pagination = query.order_by(User.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False,
    )

    operators = []

    for user in pagination.items:
        operators.append(
            {
                "id_user": user.id_user,
                "nama_lengkap": user.nama_lengkap,
                "username": user.username,
                "email": user.email,
                "nomor_telepon": user.nomor_telepon,
                "instansi": user.instansi,
                "status_aktif": user.status_aktif,
                "created_at": user.created_at,
            }
        )

    return {
        "operators": operators,
        "pagination": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "pages": pagination.pages,
            "total": pagination.total,
        },
    }


# =====================================================
# CREATE OPERATOR
# =====================================================


def create_operator_service(data):

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    nama_lengkap = data.get("nama_lengkap")
    nomor_telepon = data.get("nomor_telepon")
    instansi = data.get("instansi")

    # ===============================
    # VALIDASI
    # ===============================

    if not username:
        raise Exception("Username wajib diisi.")

    if not email:
        raise Exception("Email wajib diisi.")

    if not password:
        raise Exception("Password wajib diisi.")

    if len(password) < 8:
        raise Exception("Password minimal 8 karakter.")

    # ===============================
    # VALIDASI DUPLIKAT USERNAME
    # ===============================

    existing_username = User.query.filter_by(username=username).first()

    if existing_username:
        raise Exception("Username sudah digunakan.")

    # ===============================
    # VALIDASI DUPLIKAT EMAIL
    # ===============================

    existing_email = User.query.filter_by(email=email).first()

    if existing_email:
        raise Exception("Email sudah digunakan.")

    # ===============================
    # VALIDASI DUPLIKAT NOMOR TELEPON
    # ===============================

    if nomor_telepon:
        existing_phone = User.query.filter_by(nomor_telepon=nomor_telepon).first()

        if existing_phone:
            raise Exception("Nomor telepon sudah digunakan.")

    # ===============================
    # HASH PASSWORD
    # ===============================

    hashed_password = generate_password_hash(password).decode("utf-8")

    operator = User(
        username=username,
        password=hashed_password,
        nama_lengkap=nama_lengkap,
        email=email,
        nomor_telepon=nomor_telepon,
        instansi=instansi,
        role="operator",
        status_aktif=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    db.session.add(operator)
    db.session.commit()

    return operator.to_dict()


# =====================================================
# UPDATE OPERATOR
# =====================================================


def update_operator_service(id_user, data):

    operator = User.query.get(id_user)

    if not operator:
        raise Exception("Operator tidak ditemukan.")

    username = data.get("username", operator.username)
    email = data.get("email", operator.email)
    nomor_telepon = data.get(
        "nomor_telepon",
        operator.nomor_telepon,
    )

    # ===============================
    # VALIDASI USERNAME
    # ===============================

    existing_username = User.query.filter(
        User.username == username,
        User.id_user != id_user,
    ).first()

    if existing_username:
        raise Exception("Username sudah digunakan.")

    # ===============================
    # VALIDASI EMAIL
    # ===============================

    existing_email = User.query.filter(
        User.email == email,
        User.id_user != id_user,
    ).first()

    if existing_email:
        raise Exception("Email sudah digunakan.")

    # ===============================
    # VALIDASI NOMOR TELEPON
    # ===============================

    if nomor_telepon:
        existing_phone = User.query.filter(
            User.nomor_telepon == nomor_telepon,
            User.id_user != id_user,
        ).first()

        if existing_phone:
            raise Exception("Nomor telepon sudah digunakan.")

    # ===============================
    # UPDATE DATA
    # ===============================

    operator.nama_lengkap = data.get(
        "nama_lengkap",
        operator.nama_lengkap,
    )

    operator.username = username
    operator.email = email
    operator.nomor_telepon = nomor_telepon

    operator.instansi = data.get(
        "instansi",
        operator.instansi,
    )

    operator.updated_at = datetime.utcnow()

    # Password hanya diubah jika diisi

    if data.get("password"):
        if len(data.get("password")) < 8:
            raise Exception("Password minimal 8 karakter.")

        operator.password = generate_password_hash(data.get("password")).decode("utf-8")

    db.session.commit()

    return operator.to_dict()


# =====================================================
# UPDATE STATUS OPERATOR
# =====================================================


def update_operator_status_service(id_user, status):

    operator = User.query.get(id_user)

    if not operator:
        raise Exception("Operator tidak ditemukan.")

    operator.status_aktif = status
    operator.updated_at = datetime.utcnow()

    db.session.commit()

    return operator.to_dict()


# =====================================================
# DELETE OPERATOR
# =====================================================


def delete_operator_service(id_user):

    operator = User.query.get(id_user)

    if not operator:
        raise Exception("Operator tidak ditemukan.")

    if operator.role != "operator":
        raise Exception("User ini bukan operator.")

    db.session.delete(operator)
    db.session.commit()

    return True
