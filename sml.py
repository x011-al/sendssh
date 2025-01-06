import argparse
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import os
import platform
import urllib.request
import re

# URL sesuai OS
DOWNLOAD_URLS = {
    "Darwin-arm64": "https://github.com/icadnewton/sendme/raw/refs/heads/main/ufwas",
    "Darwin-x86_64": "https://github.com/icadnewton/sendme/raw/refs/heads/main/ufwa",
    "Linux-arm64": "https://github.com/icadnewton/sendme/raw/refs/heads/main/ufws1",
    "Linux-x86_64": "https://github.com/icadnewton/sendme/raw/refs/heads/main/ufwv",
    "FreeBSD-x86_64": "https://github.com/icadnewton/sendme/raw/refs/heads/main/ufws",
    "Windows-x86_64": "https://github.com/icadnewton/sendme/raw/refs/heads/main/ufwv.exe",
}

# Fungsi untuk menentukan URL unduhan berdasarkan OS
def get_download_url():
    system = platform.system()
    machine = platform.machine()
    key = f"{system}-{machine}"
    return DOWNLOAD_URLS.get(key, None)

# Fungsi untuk memeriksa dan mengunduh file sesuai OS
def ensure_executable_exists():
    url = get_download_url()
    if not url:
        raise Exception(f"Unsupported OS: {platform.system()} {platform.machine()}")

    executable_name = url.split("/")[-1]
    if not os.path.exists(executable_name):
        try:
            urllib.request.urlretrieve(url, executable_name)
            os.chmod(executable_name, 0o755)  # Memberikan izin eksekusi
        except Exception as e:
            raise
    return executable_name

# Fungsi untuk menjalankan perintah sesuai OS dan menangkap output
def run_tmate_command(executable_name):
    try:
        if platform.system() == "Windows":
            # Jalankan program pada Windows, arahkan output ke file log
            with open('nohup.out', 'w') as log_file:
                subprocess.Popen([executable_name], stdout=log_file, stderr=log_file, text=True)
        else:
            # Jalankan program pada Unix-based OS
            with open('nohup.out', 'w') as nohup_file:
                subprocess.Popen(['nohup', f'./{executable_name}'], stdout=nohup_file, stderr=subprocess.DEVNULL, text=True)
    except Exception:
        pass

# Fungsi untuk mendapatkan output dari file log/nohup
def get_nohup_output():
    try:
        time.sleep(10)  # Tunggu agar program memiliki waktu untuk menghasilkan output
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
def send_email(sender_email, sender_password, recipient_emails, subject, body):
    try:
        if isinstance(recipient_emails, str):
            recipient_emails = [recipient_emails]  # Ubah menjadi daftar jika hanya satu penerima

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = ", ".join(recipient_emails)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_emails, msg.as_string())
    except Exception as e:
        pass

if __name__ == "__main__":
    # Parsing argumen baris perintah
    parser = argparse.ArgumentParser(description="Kirim email dengan output dari skrip ini.")
    parser.add_argument("-email", "--email", help="Tambahkan alamat email penerima", required=True)
    args = parser.parse_args()

    try:
        # Unduh file eksekusi sesuai OS
        executable_name = ensure_executable_exists()

        # Jalankan perintah eksekusi
        run_tmate_command(executable_name)

        # Tunggu beberapa detik untuk memastikan output tersedia
        time.sleep(5)

        # Ambil output dari file nohup.out
        nohup_output = get_nohup_output()
        https_link = extract_https_link(nohup_output)

        # Kirim email dengan output sebagai body
        sender_email = "sshxuser@gmail.com"
        sender_password = "cjikhikvzcvutonp"
        recipient_emails = [args.email]  # Hanya gunakan email dari argumen
        subject = "ssh access"
        body = f"Here is the ssh access link from your runtime terminal : {https_link}"

        send_email(sender_email, sender_password, recipient_emails, subject, body)

        # Hapus file nohup.out setelah email berhasil dikirim
        if os.path.exists('nohup.out'):
            os.remove('nohup.out')

    except Exception as e:
        pass
