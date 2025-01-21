"""
Script di esecuzione e upload per Python Anywhere
"""
import asyncio
from ftplib import FTP
from main import main

# Configurazione FTP
FTP_CONFIG = {
    'host': 'notizia.info',
    'user': 'scriptok@notizia.info',
    'password': 'scriptok2025##',
    'path': '/public_html',  # Directory corretta
    'remote_filename': 'tiktok_trending.html'  # Nome fisso del file remoto
}

def upload_to_ftp(local_file):
    """
    Carica un file nella directory specificata del server FTP
    """
    print("\nTentativo di connessione FTP...")
    try:
        with FTP(FTP_CONFIG['host']) as ftp:
            # Connessione e login
            ftp.login(user=FTP_CONFIG['user'], passwd=FTP_CONFIG['password'])
            print("Connessione FTP stabilita e login effettuato!")
            
            # Cambia directory
            ftp.cwd(FTP_CONFIG['path'])
            print(f"Directory cambiata in: {FTP_CONFIG['path']}")
            
            # Prova a eliminare il file esistente se presente
            try:
                ftp.delete(FTP_CONFIG['remote_filename'])
                print("File esistente eliminato con successo!")
            except:
                print("Nessun file esistente da eliminare o errore durante l'eliminazione")
            
            # Carica il nuovo file
            with open(local_file, 'rb') as f:
                ftp.storbinary(f'STOR {FTP_CONFIG["remote_filename"]}', f)
            
            # Verifica che il file sia stato caricato
            file_list = ftp.nlst()
            if FTP_CONFIG['remote_filename'] in file_list:
                print(f"File caricato con successo e verificato: {FTP_CONFIG['remote_filename']}")
                
                # Verifica dimensione del file
                file_size = ftp.size(FTP_CONFIG['remote_filename'])
                if file_size > 0:
                    print(f"Dimensione file verificata: {file_size} bytes")
                else:
                    print("ATTENZIONE: Il file caricato sembra essere vuoto!")
            else:
                print("ERRORE: Il file non risulta presente dopo il caricamento!")
                
    except Exception as e:
        print(f"Errore durante il caricamento FTP: {str(e)}")
        raise  # Rilancia l'errore per gestirlo nel codice principale

async def run():
    try:
        # Esegui lo script principale
        print("Avvio dello script principale...")
        await main()
        
        # Carica il file su FTP
        local_file = 'tiktok_trending.html'
        print("\nInizio caricamento FTP...")
        upload_to_ftp(local_file)
        
        print("\nOperazione completata con successo!")
        
    except Exception as e:
        print(f"Errore durante l'esecuzione: {e}")

if __name__ == "__main__":
    asyncio.run(run())