import os
import sys
import getpass

from datetime import datetime

from colorama import Fore, Style, init
from sqlalchemy import text
from tabulate import tabulate
from flask_bcrypt import generate_password_hash

from app import app
from database.db import db
from models.user import User


# ==========================================
# COLORAMA
# ==========================================

init(autoreset=True)


# ==========================================
# CLEAR SCREEN
# ==========================================


def clear():
    os.system("cls" if os.name == "nt" else "clear")


# ==========================================
# PAUSE
# ==========================================


def pause():
    input(f"\n{Fore.CYAN}Tekan Enter untuk kembali...")


# ==========================================
# SUCCESS
# ==========================================


def success(message):
    print(f"\n{Fore.GREEN}✓ {message}")


# ==========================================
# ERROR
# ==========================================


def error(message):
    print(f"\n{Fore.RED}✗ {message}")


# ==========================================
# WARNING
# ==========================================


def warning(message):
    print(f"\n{Fore.YELLOW}⚠ {message}")


# ==========================================
# SYSTEM INFORMATION
# ==========================================


def get_system_info():

    try:
        with app.app_context():
            db.session.execute(text("SELECT 1"))

            return {
                "status": "Connected",
                "total_user": User.query.count(),
                "super_admin": User.query.filter_by(role="super_admin").count(),
                "operator": User.query.filter_by(role="operator").count(),
                "instansi": User.query.filter_by(role="instansi").count(),
                "nasabah": User.query.filter_by(role="nasabah").count(),
            }

    except Exception:
        return {"status": "Disconnected"}


# ==========================================
# HEADER
# ==========================================


def show_header():

    clear()

    info = get_system_info()

    print("=" * 70)
    print("        CREDIT RISK SCORING SYSTEM")
    print("         USER MANAGEMENT CLI v1.0")
    print("=" * 70)

    print("Database    : credit_risk_db")

    if info["status"] == "Connected":
        print(f"Connection  : {Fore.GREEN}Connected{Style.RESET_ALL}")

        print(f"Total User  : {info['total_user']}")
        print(f"Super Admin : {info['super_admin']}")
        print(f"Operator    : {info['operator']}")
        print(f"Instansi    : {info['instansi']}")
        print(f"Nasabah     : {info['nasabah']}")

    else:
        print(f"Connection  : {Fore.RED}Disconnected{Style.RESET_ALL}")

    sekarang = datetime.now()

    print("Tanggal     :", sekarang.strftime("%d-%m-%Y"))

    print("Jam         :", sekarang.strftime("%H:%M:%S"))

    print("=" * 70)


# ==========================================
# MENU
# ==========================================


def show_menu():

    print("1. Buat Super Admin")
    print("2. Buat Operator")
    print("3. Reset Password")
    print("4. Lihat Semua User")
    print("5. Nonaktifkan User")
    print("6. Aktifkan User")
    print("7. Hapus User")
    print("8. Keluar")

    print("=" * 70)

    return input("Pilih Menu : ").strip()


# ==========================================
# MAIN
# ==========================================


def main():

    while True:
        show_header()

        pilihan = show_menu()

        if pilihan == "1":
            create_super_admin()

        elif pilihan == "2":
            create_operator()

        elif pilihan == "3":
            reset_password()

        elif pilihan == "4":
            list_users()

        elif pilihan == "5":
            deactivate_user()

        elif pilihan == "6":
            activate_user()

        elif pilihan == "7":
            delete_user()

        elif pilihan == "8":
            print(
                f"\n{Fore.GREEN}Terima kasih telah menggunakan User Management CLI.\n"
            )

            sys.exit()

        else:
            warning("Menu tidak tersedia.")

            pause()


# ==========================================
# CREATE SUPER ADMIN
# ==========================================


def create_super_admin():

    with app.app_context():
        clear()

        print("=" * 70)
        print("                 CREATE SUPER ADMIN")
        print("=" * 70)

        # =====================================
        # HANYA BOLEH ADA 1 SUPER ADMIN
        # =====================================

        if User.query.filter_by(role="super_admin").first():
            warning("Super Admin sudah ada.")

            pause()

            return

        nama = input("Nama Lengkap        : ").strip()
        username = input("Username            : ").strip()
        email = input("Email               : ").strip()
        nomor = input("Nomor Telepon       : ").strip()

        password = getpass.getpass("Password            : ")
        confirm = getpass.getpass("Konfirmasi Password : ")

        # =====================================
        # VALIDASI
        # =====================================

        if not nama:
            error("Nama lengkap wajib diisi.")
            pause()
            return

        if not username:
            error("Username wajib diisi.")
            pause()
            return

        if not email:
            error("Email wajib diisi.")
            pause()
            return

        if "@" not in email:
            error("Format email tidak valid.")
            pause()
            return

        if len(password) < 8:
            error("Password minimal 8 karakter.")
            pause()
            return

        if password != confirm:
            error("Konfirmasi password tidak sama.")
            pause()
            return

        if User.query.filter_by(username=username).first():
            error("Username sudah digunakan.")
            pause()
            return

        if User.query.filter_by(email=email).first():
            error("Email sudah digunakan.")
            pause()
            return

        user = User(
            username=username,
            password=generate_password_hash(password).decode("utf-8"),
            nama_lengkap=nama,
            email=email,
            nomor_telepon=nomor,
            role="super_admin",
            instansi="System",
            status_aktif=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        db.session.add(user)
        db.session.commit()

        success("Super Admin berhasil dibuat.")

        print("\nInformasi Akun")
        print("-" * 70)
        print(f"ID User      : {user.id_user}")
        print(f"Nama         : {user.nama_lengkap}")
        print(f"Username     : {user.username}")
        print(f"Email        : {user.email}")
        print(f"Role         : {user.role}")
        print(f"Status       : Aktif")

        pause()


# ==========================================
# CREATE OPERATOR
# ==========================================


def create_operator():

    with app.app_context():
        clear()

        print("=" * 70)
        print("                   CREATE OPERATOR")
        print("=" * 70)

        nama = input("Nama Lengkap        : ").strip()
        username = input("Username            : ").strip()
        email = input("Email               : ").strip()
        nomor = input("Nomor Telepon       : ").strip()
        instansi = input("Nama Instansi       : ").strip()

        password = getpass.getpass("Password            : ")
        confirm = getpass.getpass("Konfirmasi Password : ")

        # =====================================
        # VALIDASI
        # =====================================

        if not nama:
            error("Nama lengkap wajib diisi.")
            pause()
            return

        if not username:
            error("Username wajib diisi.")
            pause()
            return

        if not email:
            error("Email wajib diisi.")
            pause()
            return

        if not instansi:
            error("Nama instansi wajib diisi.")
            pause()
            return

        if "@" not in email:
            error("Format email tidak valid.")
            pause()
            return

        if len(password) < 8:
            error("Password minimal 8 karakter.")
            pause()
            return

        if password != confirm:
            error("Konfirmasi password tidak sama.")
            pause()
            return

        if User.query.filter_by(username=username).first():
            error("Username sudah digunakan.")
            pause()
            return

        if User.query.filter_by(email=email).first():
            error("Email sudah digunakan.")
            pause()
            return

        operator = User(
            username=username,
            password=generate_password_hash(password).decode("utf-8"),
            nama_lengkap=nama,
            email=email,
            nomor_telepon=nomor,
            role="operator",
            instansi=instansi,
            status_aktif=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )

        db.session.add(operator)
        db.session.commit()

        success("Operator berhasil dibuat.")

        print("\nInformasi Akun")
        print("-" * 70)
        print(f"ID User      : {operator.id_user}")
        print(f"Nama         : {operator.nama_lengkap}")
        print(f"Username     : {operator.username}")
        print(f"Email        : {operator.email}")
        print(f"Instansi     : {operator.instansi}")
        print(f"Role         : {operator.role}")
        print(f"Status       : Aktif")

        pause()


# ==========================================
# LIST USERS
# ==========================================


def list_users():

    with app.app_context():
        clear()

        print("=" * 120)
        print("                     DAFTAR USER")
        print("=" * 120)

        users = User.query.order_by(User.id_user.asc()).all()

        if not users:
            warning("Belum ada user.")

            pause()

            return

        table = []

        for user in users:
            table.append(
                [
                    user.id_user,
                    user.nama_lengkap,
                    user.username,
                    user.email,
                    user.role,
                    user.instansi if user.instansi else "-",
                    "Aktif" if user.status_aktif else "Nonaktif",
                    user.terakhir_login.strftime("%d-%m-%Y %H:%M")
                    if user.terakhir_login
                    else "-",
                    user.created_at.strftime("%d-%m-%Y") if user.created_at else "-",
                ]
            )

        print(
            tabulate(
                table,
                headers=[
                    "ID",
                    "Nama",
                    "Username",
                    "Email",
                    "Role",
                    "Instansi",
                    "Status",
                    "Last Login",
                    "Created",
                ],
                tablefmt="fancy_grid",
            )
        )

        print()

        print(f"Total User : {len(users)}")

        pause()


# ==========================================
# RESET PASSWORD
# ==========================================


def reset_password():

    with app.app_context():
        clear()

        print("=" * 70)
        print("                 RESET PASSWORD")
        print("=" * 70)

        username = input("Username : ").strip()

        user = User.query.filter_by(username=username).first()

        if not user:
            error("User tidak ditemukan.")

            pause()

            return

        print()

        print(f"Nama     : {user.nama_lengkap}")
        print(f"Role     : {user.role}")
        print(f"Email    : {user.email}")

        print("-" * 70)

        password = getpass.getpass("Password Baru       : ")

        confirm = getpass.getpass("Konfirmasi Password : ")

        if len(password) < 8:
            error("Password minimal 8 karakter.")

            pause()

            return

        if password != confirm:
            error("Konfirmasi password tidak sama.")

            pause()

            return

        user.password = generate_password_hash(password).decode("utf-8")

        user.updated_at = datetime.utcnow()

        db.session.commit()

        success("Password berhasil diperbarui.")

        pause()
# ==========================================
# DEACTIVATE USER
# ==========================================

def deactivate_user():

    with app.app_context():

        clear()

        print("=" * 70)
        print("               NONAKTIFKAN USER")
        print("=" * 70)

        username = input("Username : ").strip()

        user = User.query.filter_by(
            username=username
        ).first()

        if not user:

            error("User tidak ditemukan.")

            pause()

            return

        if user.role == "super_admin":

            error("Super Admin tidak dapat dinonaktifkan.")

            pause()

            return

        if not user.status_aktif:

            warning("User sudah nonaktif.")

            pause()

            return

        print()

        print(f"Nama      : {user.nama_lengkap}")
        print(f"Role      : {user.role}")
        print(f"Instansi  : {user.instansi}")
        print(f"Status    : Aktif")

        print("-" * 70)

        konfirmasi = input(
            "Ketik YES untuk menonaktifkan : "
        )

        if konfirmasi != "YES":

            warning("Proses dibatalkan.")

            pause()

            return

        user.status_aktif = False
        user.updated_at = datetime.utcnow()

        db.session.commit()

        success("User berhasil dinonaktifkan.")

        pause()


# ==========================================
# ACTIVATE USER
# ==========================================

def activate_user():

    with app.app_context():

        clear()

        print("=" * 70)
        print("                 AKTIFKAN USER")
        print("=" * 70)

        username = input("Username : ").strip()

        user = User.query.filter_by(
            username=username
        ).first()

        if not user:

            error("User tidak ditemukan.")

            pause()

            return

        if user.status_aktif:

            warning("User sudah aktif.")

            pause()

            return

        print()

        print(f"Nama      : {user.nama_lengkap}")
        print(f"Role      : {user.role}")
        print(f"Instansi  : {user.instansi}")

        print("-" * 70)

        konfirmasi = input(
            "Ketik YES untuk mengaktifkan : "
        )

        if konfirmasi != "YES":

            warning("Proses dibatalkan.")

            pause()

            return

        user.status_aktif = True
        user.updated_at = datetime.utcnow()

        db.session.commit()

        success("User berhasil diaktifkan.")

        pause()


# ==========================================
# DELETE USER
# ==========================================

def delete_user():

    with app.app_context():

        clear()

        print("=" * 70)
        print("                  HAPUS USER")
        print("=" * 70)

        username = input("Username : ").strip()

        user = User.query.filter_by(
            username=username
        ).first()

        if not user:

            error("User tidak ditemukan.")

            pause()

            return

        if user.role == "super_admin":

            error("Super Admin tidak boleh dihapus.")

            pause()

            return

        print()

        print("Informasi User")

        print("-" * 70)

        print(f"ID         : {user.id_user}")
        print(f"Nama       : {user.nama_lengkap}")
        print(f"Username   : {user.username}")
        print(f"Role       : {user.role}")
        print(f"Instansi   : {user.instansi}")
        print(
            f"Status     : {'Aktif' if user.status_aktif else 'Nonaktif'}"
        )

        print("-" * 70)

        print(
            f"{Fore.RED}PERINGATAN!"
        )

        print(
            "Data user akan dihapus permanen."
        )

        confirm = input(
            "\nKetik DELETE untuk melanjutkan : "
        )

        if confirm != "DELETE":

            warning("Penghapusan dibatalkan.")

            pause()

            return

        db.session.delete(user)

        db.session.commit()

        success("User berhasil dihapus.")

        pause()