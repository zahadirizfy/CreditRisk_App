from datetime import timedelta


class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/credit_risk_db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "credit-risk-secret-key"

    # Token berlaku selama 7 hari
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
