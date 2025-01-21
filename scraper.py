"""
Gestione dello scraping dei video TikTok
"""
from typing import Dict, List, Optional
import json
import time
import requests
from playwright.async_api import async_playwright
from config import CONFIG, BROWSER_CONFIG, API_CONFIG

class TikTokScraper:
    def __init__(self):
        self.config = CONFIG
        self.browser_config = BROWSER_CONFIG
        self.api_config = API_CONFIG
        self.headers = {
            'User-Agent': BROWSER_CONFIG['user_agent'],
            'Accept': 'application/json',
            'Referer': API_CONFIG['base_referer']
        }

    async def extract_auth_params(self) -> Optional[Dict[str, str]]:
        """Estrae i parametri di autenticazione necessari"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()
            
            await page.goto("https://www.tiktok.com/explore")
            await page.wait_for_timeout(2000)
            
            # Estrai i parametri necessari
            ms_token = await page.evaluate("localStorage.getItem('msToken')")
            
            await browser.close()
            
            if ms_token:
                return {
                    'timestamp': str(int(time.time())),
                    'user-sign': ms_token,
                    'web-id': ms_token
                }
            return None

    def fetch_tiktok_page(self, page: int, params: Dict, headers: Dict) -> List[Dict]:
        """Recupera una singola pagina di video"""
        params = params.copy()
        params['page'] = str(page)

        try:
            response = requests.get(
                self.api_config['trend_list_url'],
                headers=headers,
                params=params,
                timeout=7
            )
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and isinstance(data['data'], dict):
                    videos = data['data'].get('videos', [])
                    print(f"Pagina {page} caricata")
                    return videos
                return []
        except Exception as e:
            print(f"Errore pagina {page}: {str(e)}")
            return []

    def extract_video_data(self, url: str) -> Optional[Dict]:
        """Estrae i dati di un singolo video"""
        try:
            response = requests.get(url, headers=self.headers)
            if not response.ok:
                return {
                    'titolo': 'Video non disponibile',
                    'creator': 'N/A',
                    'url': url,
                    'views': 'N/A',
                    'categorie': 'N/A',
                    'keywords': 'N/A'
                }
            
            # Estrai le informazioni dalla pagina
            text = response.text
            start_idx = text.find('"ItemModule":') + 13
            end_idx = text.find(',"UserModule"')
            if start_idx > 12 and end_idx > 0:
                json_str = text[start_idx:end_idx]
                item_data = json.loads(json_str)
                
                # Prendi il primo video
                video_id = list(item_data.keys())[0]
                video_info = item_data[video_id]
                
                return {
                    'titolo': video_info.get('desc', 'N/A'),
                    'creator': video_info.get('author', {}).get('nickname', 'N/A'),
                    'url': url,
                    'views': self.format_number(video_info.get('stats', {}).get('playCount', 'N/A')),
                    'categorie': 'N/A',
                    'keywords': 'N/A'
                }
                
        except Exception as e:
            print(f"Errore nell'estrazione dei dati per {url}: {str(e)}")
            return None

    @staticmethod
    def format_number(num):
        """Formatta i numeri con i separatori delle migliaia"""
        try:
            return "{:,}".format(int(num)).replace(",", ".")
        except:
            return str(num)
