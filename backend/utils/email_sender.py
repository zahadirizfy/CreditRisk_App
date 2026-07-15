import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()


def send_reset_email(to_email, otp_code):

    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

    pesan = f"""
    Halo,
    
    Kami menerima permintaan untuk mereset password akun Anda.
    Berikut adalah kode OTP Anda: {otp_code}
    
    Kode ini hanya berlaku selama 15 menit. Jika Anda tidak merasa meminta reset password, abaikan email ini.
    
    Terima kasih,
    Tim Admin
    """

    msg = MIMEText(pesan)
    msg["Subject"] = "Kode Reset Password"
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email

    try:
        # Menghubungkan ke server SMTP Gmail
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Gagal mengirim email: {e}")
        return False
