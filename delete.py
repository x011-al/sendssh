import time
from imapclient import IMAPClient

# Konfigurasi
IMAP_SERVER = 'imap.gmail.com'
EMAIL_ADDRESS = 'sshxuser@gmail.com'
EMAIL_PASSWORD = 'cjikhikvzcvutonp'
FOLDER_SENT = '[Gmail]/Sent Mail'  # Untuk Gmail biasanya "Sent Mail", bisa juga "[Gmail]/Surat Terkirim"

def delete_sent_mail():
    try:
        with IMAPClient(IMAP_SERVER) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            print(f"Menghapus semua email di folder: {FOLDER_SENT}...\n")

            server.select_folder(FOLDER_SENT)  # Pilih folder terkirim
            messages = server.search(['ALL'])  # Ambil semua email

            if not messages:
                print("Tidak ada email untuk dihapus.")
                return

            # Tandai semua pesan untuk dihapus
            server.delete_messages(messages)
            server.expunge()

            print(f"Berhasil menghapus {len(messages)} email dari folder terkirim.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    delete_sent_mail()
