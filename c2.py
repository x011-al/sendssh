import re
import time
from imapclient import IMAPClient
from email import message_from_bytes
from datetime import datetime

# Konfigurasi
IMAP_SERVER = 'imap.gmail.com'
EMAIL_ADDRESS = 'sshxuser@gmail.com'
EMAIL_PASSWORD = 'cjikhikvzcvutonp'
FOLDER_SENT = '[Gmail]/Surat Terkirim'

def monitor_sent_mail():
    last_processed_id = 0  # Menyimpan ID pesan terakhir yang diproses

    try:
        with IMAPClient(IMAP_SERVER) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            print(f"Memantau folder: {FOLDER_SENT} setiap 5 detik...\n")

            while True:
                server.select_folder(FOLDER_SENT, readonly=True)  # Pilih folder terkirim
                messages = server.search(['ALL'])  # Ambil semua email
                messages = sorted(messages, reverse=True)  # Urutkan dari email terbaru

                for msg_id in messages:
                    if msg_id <= last_processed_id:
                        break  # Hentikan jika ID pesan sudah diproses sebelumnya

                    msg_data = server.fetch(msg_id, ['ENVELOPE', 'BODY[]'])
                    envelope = msg_data[msg_id][b'ENVELOPE']
                    raw_email = msg_data[msg_id][b'BODY[]']

                    # Mengurai email mentah menjadi format yang dapat dibaca
                    email_message = message_from_bytes(raw_email)

                    to_address = f"{envelope.to[0].mailbox.decode()}@{envelope.to[0].host.decode()}" if envelope.to else "(Tidak ada penerima)"
                    date_time = envelope.date.strftime("%d-%m-%Y %H:%M:%S")  # Format tanggal dan waktu
                    links = extract_links(email_message)

                    # Tampilkan hanya jika ada link
                    if links:
                        print(f"Dikirim ke: {to_address}")
                        print(f"Datetime: {date_time}")
                        print("email:")
                        for link in links:
                            print(f"- {link}")
                        print("-" * 50)

                # Perbarui ID pesan terakhir yang diproses
                if messages:
                    last_processed_id = max(messages)

                time.sleep(5)  # Tunggu 5 detik sebelum pengecekan ulang

    except Exception as e:
        print(f"Error: {e}")

def extract_links(email_message):
    """
    Ekstrak semua link HTTPS dari isi email.
    """
    links = []
    if email_message.is_multipart():
        for part in email_message.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain" or content_type == "text/html":
                payload = part.get_payload(decode=True).decode().strip()
                links.extend(re.findall(r'https?://\S+', payload))  # Cari semua link
    else:
        payload = email_message.get_payload(decode=True).decode().strip()
        links.extend(re.findall(r'https?://\S+', payload))  # Cari semua link

    return links

if __name__ == "__main__":
    monitor_sent_mail()
