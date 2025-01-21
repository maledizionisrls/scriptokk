"""
Configurazioni globali per il sistema di scraping TikTok
"""

# Configurazione principale
CONFIG = {
    'PAGES_TO_ANALYZE': 27,     # Numero di pagine da analizzare (max 27)
    'OUTPUT_VIDEOS': 50,        # Numero di video da includere nel risultato finale
    'COUNTRY_CODE': 'IT',       # Codice paese
    'TIME_PERIOD': '7',         # Periodo in giorni
    'PAGE_SIZE': 20,           # Video per pagina
    'DELAY': 0.05,             # Delay tra le richieste in secondi
    'MAX_AUTH_RETRIES': 3,     # Numero massimo di tentativi per l'autenticazione
    'AUTH_RETRY_DELAY': 2,     # Secondi di attesa tra i tentativi di autenticazione
    'OUTPUT_FILENAME': 'tiktok_trending.html'  # Nome fisso del file di output
}

# Configurazione browser
BROWSER_CONFIG = {
    'viewport': {'width': 1920, 'height': 1080},
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

# Configurazione API endpoints
API_CONFIG = {
    'trend_list_url': "https://ads.tiktok.com/creative_radar_api/v1/popular_trend/list",
    'base_referer': "https://ads.tiktok.com/business/creativecenter/inspiration/popular/pc/en"
}