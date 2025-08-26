import time
from imapclient import IMAPClient

# Konfigurasi
IMAP_SERVER = 'imap.gmail.com'
EMAIL_ADDRESS = 'sshxuser@gmail.com'
EMAIL_PASSWORD = 'cjikhikvzcvutonp'

def delete_sent_mail():
    try:
        with IMAPClient(IMAP_SERVER) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

            # Tampilkan semua folder untuk debug
            folders = server.list_folders()
            print("Daftar folder tersedia:")
            for f in folders:
                print(f)

            # Coba deteksi folder terkirim (Sent Mail / Surat Terkirim)
            possible_folders = ['[Gmail]/Sent Mail', '[Gmail]/Surat Terkirim', 'Sent', 'Sent Items']
            sent_folder = None
            for _, _, name in folders:
                if name in possible_folders:
                    sent_folder = name
                    break

            if not sent_folder:
                print("Folder terkirim tidak ditemukan. Cek daftar folder di atas.")
                return

            print(f"\nMenghapus semua email di folder: {sent_folder}...\n")
            server.select_folder(sent_folder)

            messages = server.search(['ALL'])
            if not messages:
                print("Tidak ada email untuk dihapus.")
                return

            server.delete_messages(messages)
            server.expunge()

            print(f"Berhasil menghapus {len(messages)} email dari folder {sent_folder}.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    delete_sent_mail()
