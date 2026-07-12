from datetime import datetime

from sqlalchemy import or_, func
from flask_bcrypt import generate_password_hash

from database.db import db
from models.user import User
from services.dashboard_service import dashboard_service


# =====================================================
# GET CUSTOMER
# =====================================================

def get_customers_service(page, per_page, search):

    query = User.query.filter(
        User.role.in_(["nasabah", "instansi"])
    )

    # ===============================
    # SEARCH
    # ===============================

    if search:

        query = query.filter(
            or_(
                User.nama_lengkap.ilike(f"%{search}%"),
                User.username.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
                User.nomor_telepon.ilike(f"%{search}%"),
                User.instansi.ilike(f"%{search}%"),
            )
        )

    # ===============================
    # PAGINATION
    # ===============================

    pagination = query.order_by(
        User.created_at.desc()
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False,
    )

    customers = []

    for user in pagination.items:

        customers.append(
            {
                "id_user": user.id_user,
                "nama_lengkap": user.nama_lengkap,
                "username": user.username,
                "email": user.email,
                "nomor_telepon": user.nomor_telepon,
                "role": user.role,
                "instansi": user.instansi,
                "status_aktif": user.status_aktif,
                "created_at": user.created_at,
            }
        )

    return {
        "customers": customers,
        "pagination": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "pages": pagination.pages,
            "total": pagination.total,
        },
    }


# =====================================================
# GET CUSTOMER BY ID
# =====================================================

def get_customer_by_id_service(id_user):

    customer = User.query.filter(
        User.id_user == id_user,
        User.role.in_(["nasabah", "instansi"]),
    ).first()

    if not customer:
        raise Exception("Nasabah / Instansi tidak ditemukan.")

    return customer.to_dict()


# =====================================================
# CREATE CUSTOMER
# =====================================================

def create_customer_service(data):

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    nama_lengkap = data.get("nama_lengkap")
    nomor_telepon = data.get("nomor_telepon")
    instansi = data.get("instansi")
    role = data.get("role")

    # ===============================
    # VALIDASI DATA
    # ===============================

    if not username:
        raise Exception("Username wajib diisi.")

    if not email:
        raise Exception("Email wajib diisi.")

    if not password:
        raise Exception("Password wajib diisi.")

    if len(password) < 8:
        raise Exception("Password minimal 8 karakter.")

    if not nama_lengkap:
        raise Exception("Nama lengkap wajib diisi.")

    if role not in ["nasabah", "instansi"]:
        raise Exception("Role tidak valid.")

    if role == "instansi" and not instansi:
        raise Exception("Nama instansi wajib diisi.")

    # ===============================
    # VALIDASI USERNAME
    # ===============================

    existing_username = User.query.filter_by(
        username=username
    ).first()

    if existing_username:
        raise Exception("Username sudah digunakan.")

    # ===============================
    # VALIDASI EMAIL
    # ===============================

    existing_email = User.query.filter_by(
        email=email
    ).first()

    if existing_email:
        raise Exception("Email sudah digunakan.")

    # ===============================
    # VALIDASI NOMOR TELEPON
    # ===============================

    if nomor_telepon:

        existing_phone = User.query.filter_by(
            nomor_telepon=nomor_telepon
        ).first()

        if existing_phone:
            raise Exception("Nomor telepon sudah digunakan.")

    # ===============================
    # HASH PASSWORD
    # ===============================

    hashed_password = generate_password_hash(
        password
    ).decode("utf-8")

    # ===============================
    # SIMPAN DATA
    # ===============================

    customer = User(
        username=username,
        password=hashed_password,
        nama_lengkap=nama_lengkap,
        email=email,
        nomor_telepon=nomor_telepon,
        instansi=instansi if role == "instansi" else None,
        role=role,
        status_aktif=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )

    db.session.add(customer)
    db.session.commit()

    return customer.to_dict()


# =====================================================
# UPDATE CUSTOMER
# =====================================================

def update_customer_service(id_user, data):

    customer = User.query.filter(
        User.id_user == id_user,
        User.role.in_(["nasabah", "instansi"])
    ).first()

    if not customer:
        raise Exception("Data tidak ditemukan.")

    username = data.get(
        "username",
        customer.username,
    )

    email = data.get(
        "email",
        customer.email,
    )

    nomor_telepon = data.get(
        "nomor_telepon",
        customer.nomor_telepon,
    )

    role = data.get(
        "role",
        customer.role,
    )

    instansi = data.get(
        "instansi",
        customer.instansi,
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
    # VALIDASI ROLE
    # ===============================

    if role not in ["nasabah", "instansi"]:
        raise Exception("Role tidak valid.")

    if role == "instansi" and not instansi:
        raise Exception("Nama instansi wajib diisi.")

    # ===============================
    # UPDATE DATA
    # ===============================

    customer.nama_lengkap = data.get(
        "nama_lengkap",
        customer.nama_lengkap,
    )

    customer.username = username

    customer.email = email

    customer.nomor_telepon = nomor_telepon

    customer.role = role

    customer.instansi = (
        instansi if role == "instansi" else None
    )

    customer.updated_at = datetime.utcnow()

    # ===============================
    # UPDATE PASSWORD
    # ===============================

    if data.get("password"):

        if len(data.get("password")) < 8:
            raise Exception("Password minimal 8 karakter.")

        customer.password = generate_password_hash(
            data.get("password")
        ).decode("utf-8")

    db.session.commit()

    return customer.to_dict()

# =====================================================
# UPDATE STATUS CUSTOMER
# =====================================================

def update_customer_status_service(id_user, status):

    customer = User.query.filter(
        User.id_user == id_user,
        User.role.in_(["nasabah", "instansi"]),
    ).first()

    if not customer:
        raise Exception("Nasabah / Instansi tidak ditemukan.")

    customer.status_aktif = bool(status)

    customer.updated_at = datetime.utcnow()

    db.session.commit()

    return customer.to_dict()


# =====================================================
# DELETE CUSTOMER
# =====================================================

def delete_customer_service(id_user):

    customer = User.query.filter(
        User.id_user == id_user,
        User.role.in_(["nasabah", "instansi"]),
    ).first()

    if not customer:
        raise Exception("Nasabah / Instansi tidak ditemukan.")

    db.session.delete(customer)

    db.session.commit()

    return True


# =====================================================
# DASHBOARD CUSTOMER
# =====================================================

def get_customer_dashboard_service():

    # =====================================================
    # AMBIL DASHBOARD ADMIN
    # =====================================================

    data = dashboard_service()

    # =====================================================
    # TOTAL CUSTOMER
    # =====================================================

    total_customer = User.query.filter(
        User.role.in_(["nasabah", "instansi"])
    ).count()

    data["total_user"] = total_customer

    # =====================================================
    # DISTRIBUSI CUSTOMER
    # =====================================================

    distribution = (
        db.session.query(
            User.role,
            func.count(User.id_user),
        )
        .filter(
            User.role.in_(["nasabah", "instansi"])
        )
        .group_by(User.role)
        .all()
    )

    data["user_distribution"] = {
        role: total
        for role, total in distribution
    }

    return data
