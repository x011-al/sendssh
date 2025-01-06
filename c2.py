from imapclient import IMAPClient
import time

# Konfigurasi
IMAP_SERVER = 'imap.gmail.com'
EMAIL_ADDRESS = 'sshxuser@gmail.com'
EMAIL_PASSWORD = 'cjikhikvzcvutonp'

def monitor_emails(folder_name):
    try:
        with IMAPClient(IMAP_SERVER) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.select_folder(folder_name, readonly=True)

            print(f"Memantau folder: {folder_name}...")
            seen_messages = set()  # Menyimpan ID pesan yang sudah diproses
            while True:
                messages = server.search(['UNSEEN'])  # Cari email yang belum dibaca
                for msg_id in messages:
                    if msg_id not in seen_messages:
                        seen_messages.add(msg_id)
                        msg_data = server.fetch(msg_id, ['ENVELOPE'])
                        envelope = msg_data[msg_id][b'ENVELOPE']

                        from_address = f"{envelope.from_[0].mailbox.decode()}@{envelope.from_[0].host.decode()}"
                        subject = envelope.subject.decode() if envelope.subject else "(Tanpa Subjek)"
                        print(f"\n[Folder: {folder_name}]")
                        print(f"Dari: {from_address}")
                        print(f"Subjek: {subject}")

                time.sleep(10)  # Periksa setiap 10 detik
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Memantau email masuk dan keluar
    print("1. Memantau email masuk (INBOX)")
    monitor_emails('INBOX')  # Memantau folder INBOX untuk email masuk

    print("2. Memantau email keluar (Sent Mail)")
    monitor_emails('[Gmail]/Sent Mail')  # Memantau folder Sent Mail untuk email keluar
