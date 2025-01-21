"""
Gestione dei template HTML per la visualizzazione dei video
"""
import json
from typing import List, Dict

class HTMLGenerator:
    @staticmethod
    def get_html_template(videos_data: List[Dict]) -> str:
        html_start = '''<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TikTok Trending Videos</title>
    <style>
        * { box-sizing: border-box; }
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f0f2f5; }
        .container { max-width: 1400px; margin: 0 auto; }
        .grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px; 
            padding: 20px;
        }
        .video-card { 
            background: white; 
            border-radius: 8px; 
            padding: 15px; 
            margin-bottom: 20px; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
        }
        .video-title { font-size: 16px; font-weight: bold; margin-bottom: 10px; }
        .video-stats { margin-bottom: 15px; font-size: 14px; }
        .video-url {
            font-size: 13px;
            word-break: break-all;
            margin-bottom: 10px;
        }
        .video-url a {
            color: #2196F3;
            text-decoration: none;
        }
        .video-url a:hover {
            text-decoration: underline;
        }
        .video-container {
            width: 100%;
            position: relative;
            margin-bottom: 15px;
        }
        .video-embed {
            position: relative;
            padding-bottom: 177.77%;
            height: 0;
            overflow: hidden;
            border-radius: 4px;
        }
        .video-embed iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
            background: #f8f8f8;
        }
        .tag { 
            display: inline-block; 
            background: #e1e4e8; 
            padding: 4px 8px; 
            border-radius: 4px; 
            margin: 2px; 
            font-size: 12px;
            color: #444;
        }
        .header { 
            text-align: center; 
            padding: 20px; 
            margin-bottom: 20px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .pagination {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin: 20px 0;
        }
        .pagination button {
            padding: 8px 16px;
            border: none;
            background: #2196F3;
            color: white;
            border-radius: 4px;
            cursor: pointer;
        }
        .pagination button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        .pagination-info {
            text-align: center;
            margin: 10px 0;
        }
        @media (max-width: 768px) {
            .grid { grid-template-columns: 1fr; }
            body { padding: 10px; }
            .video-card { margin-bottom: 15px; }
        }
        
        @media (min-width: 769px) and (max-width: 1200px) {
            .grid { grid-template-columns: repeat(2, 1fr); }
        }
        
        @media (min-width: 1201px) {
            .grid { grid-template-columns: repeat(3, 1fr); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>TikTok Trending Videos</h1>
            <p>Top trending videos in Italy</p>
        </div>
        <div class="pagination"></div>
        <div class="pagination-info"></div>
        <div class="grid" id="videos-container">
        </div>
        <div class="pagination"></div>
    </div>
    <script>'''

        videos_json = json.dumps([{
            'id': video['url'].split('/')[-1],
            'title': video['titolo'],
            'creator': video['creator'],
            'views': video['views'],
            'url': video['url'],
            'categories': [cat for cat in video['categorie'].split(', ') if cat != 'N/A'],
            'keywords': [kw for kw in video['keywords'].split(', ') if kw != 'N/A']
        } for video in videos_data])

        html_middle = f'''
        // Configurazione
        const VIDEOS_PER_PAGE = 10;
        const videos = {videos_json};

        // Stato corrente
        let currentPage = 1;
        const totalPages = Math.ceil(videos.length / VIDEOS_PER_PAGE);

        // Gestione Intersection Observer per lazy loading
        const videoObserver = new IntersectionObserver((entries, observer) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    const container = entry.target;
                    const iframe = container.querySelector('iframe');
                    if (iframe.dataset.src) {{
                        iframe.src = iframe.dataset.src;
                        iframe.removeAttribute('data-src');
                        observer.unobserve(container);
                    }}
                }}
            }});
        }}, {{
            rootMargin: '50px 0px',
            threshold: 0.1
        }});

        function createVideoCard(video) {{
            const categories = video.categories.map(cat => 
                `<span class="tag">${{cat}}</span>`).join(' ') || 'None';
            const keywords = video.keywords.map(kw => 
                `<span class="tag">${{kw}}</span>`).join(' ') || 'None';
            
            const card = document.createElement('div');
            card.className = 'video-card';
            card.innerHTML = `
                <div class="video-title">${{video.title}}</div>
                <div class="video-stats">
                    <strong>Creator:</strong> ${{video.creator}}<br>
                    <strong>Views:</strong> ${{video.views}}
                </div>
                <div class="video-url">
                    <strong>URL:</strong> <a href="${{video.url}}" target="_blank">${{video.url}}</a>
                </div>
                <div class="video-container">
                    <div class="video-embed">
                        <iframe data-src="https://www.tiktok.com/embed/${{video.id}}" 
                                allowfullscreen scrolling="no" 
                                allow="encrypted-media;">
                        </iframe>
                    </div>
                </div>
                <div class="metadata">
                    <strong>Categories:</strong><br>
                    ${{categories}}
                </div>
                <div class="metadata" style="margin-top: 10px;">
                    <strong>Keywords:</strong><br>
                    ${{keywords}}
                </div>
            `;
            return card;
        }}

        function updatePagination() {{
            const paginationElements = document.querySelectorAll('.pagination');
            const paginationHTML = `
                <button onclick="changePage(1)" ${{currentPage === 1 ? 'disabled' : ''}}>First</button>
                <button onclick="changePage(${{currentPage - 1}})" ${{currentPage === 1 ? 'disabled' : ''}}>Previous</button>
                <button onclick="changePage(${{currentPage + 1}})" ${{currentPage === totalPages ? 'disabled' : ''}}>Next</button>
                <button onclick="changePage(${{totalPages}})" ${{currentPage === totalPages ? 'disabled' : ''}}>Last</button>
            `;
            paginationElements.forEach(el => el.innerHTML = paginationHTML);
            
            document.querySelector('.pagination-info').textContent = 
                `Page ${{currentPage}} of ${{totalPages}} (${{videos.length}} videos total)`;
        }}

        function changePage(newPage) {{
            if (newPage < 1 || newPage > totalPages) return;
            currentPage = newPage;
            displayCurrentPage();
            updatePagination();
            window.scrollTo(0, 0);
        }}

        function displayCurrentPage() {{
            const container = document.getElementById('videos-container');
            container.innerHTML = '';
            
            const start = (currentPage - 1) * VIDEOS_PER_PAGE;
            const end = start + VIDEOS_PER_PAGE;
            const pageVideos = videos.slice(start, end);
            
            pageVideos.forEach(video => {{
                const card = createVideoCard(video);
                container.appendChild(card);
                videoObserver.observe(card.querySelector('.video-container'));
            }});
        }}

        // Inizializzazione
        displayCurrentPage();
        updatePagination();
    </script>
</body>
</html>'''

        return html_start + html_middle

    @staticmethod
    def generate_html_file(videos_data: List[Dict], output_filename: str):
        """Genera il file HTML con i video"""
        html_content = HTMLGenerator.get_html_template(videos_data)
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)