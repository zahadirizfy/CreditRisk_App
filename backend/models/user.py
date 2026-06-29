from database.db import db
from datetime import datetime


class User(db.Model):

    __tablename__ = "users"
    
    predictions = db.relationship(
    "Prediction",
    backref="user",
    lazy=True
    )

    id_user = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    nama_lengkap = db.Column(
        db.String(30)
    )

    email = db.Column(
        db.String(100),
        unique=True
    )

    nomor_telepon = db.Column(
        db.String(15)
    )

    role = db.Column(
        db.String(20),
        nullable=False
    )

    institusi = db.Column(
        db.String(40)
    )

    status_aktif = db.Column(
        db.Boolean,
        default=True
    )

    terakhir_login = db.Column(
        db.DateTime
    )

    created_at = db.Column(
    db.DateTime,
    default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
        
    )

    def to_dict(self):
        return {
            "id_user": self.id_user,
            "username": self.username,
            "nama_lengkap": self.nama_lengkap,
            "email": self.email,
            "nomor_telepon": self.nomor_telepon,
            "role": self.role,
            "institusi": self.institusi,
            "status_aktif": self.status_aktif,
            "terakhir_login": self.terakhir_login,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }