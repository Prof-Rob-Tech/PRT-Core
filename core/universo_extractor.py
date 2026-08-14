"""
===========================================================
PRT Labs - Core / Extractors
Class: UniversoExtractor

Description:
    Extrator de mídias embutidas para a plataforma Universo Técnico.
    Autentica no WordPress da plataforma, analisa o HTML da página
    da aula e extrai automaticamente o player de vídeo (Panda Video,
    Vimeo, Bunny CDN, VTurb, HLS .m3u8, etc.).
===========================================================
"""

import re
from typing import Dict, Tuple, Optional
import requests


class UniversoExtractor:
    """Extrator de links reais de vídeo para o Universo Técnico."""

    def __init__(self, username: Optional[str] = None, password: Optional[str] = None) -> None:
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        })

    def login(self, login_url: str = "https://universotecnico.com/wp-login.php") -> bool:
        """Realiza o login no WordPress do Universo Técnico."""
        if not self.username or not self.password:
            print("⚠️ [UniversoExtractor] Usuário ou senha não informados.")
            return False

        try:
            # 1. Carrega a página inicial de login para capturar cookies e campos ocultos
            res_get = self.session.get(login_url, timeout=15)
            
            payload = {
                "log": self.username,
                "pwd": self.password,
                "wp-submit": "Acessar",
                "testcookie": "1",
                "rememberme": "forever"
            }

            # Verifica se há campo 'redirect_to' dinâmico no formulário HTML
            redirect_match = re.search(r'name=["\']redirect_to["\']\s+value=["\']([^"\']+)["\']', res_get.text)
            if redirect_match:
                payload["redirect_to"] = redirect_match.group(1)

            # 2. Envia a requisição de POST de login
            res_post = self.session.post(login_url, data=payload, timeout=15)

            cookies_dict = self.session.cookies.get_dict()
            is_logged = any("wordpress_logged_in" in k for k in cookies_dict.keys()) or res_post.status_code in [200, 302]

            if is_logged:
                print("🔑 [UniversoExtractor] Login efetuado com sucesso!")
                return True
            else:
                print("❌ [UniversoExtractor] Não foi possível autenticar com o usuário e senha fornecidos.")

        except Exception as e:
            print(f"⚠️ [UniversoExtractor] Erro durante login no WordPress: {e}")

        return False

    def extract_video_url(self, page_url: str) -> Tuple[str, Dict[str, str]]:
        """
        Acessa a página da aula e extrai a URL real do vídeo embutido no iframe.
        Retorna (video_url, headers).
        """
        headers_extra = {
            "Referer": "https://universotecnico.com/",
            "User-Agent": self.session.headers["User-Agent"]
        }

        if self.username and self.password:
            self.login()

        try:
            print(f"🔍 [UniversoExtractor] Analisando HTML da aula: {page_url}")
            resp = self.session.get(page_url, timeout=20)
            html = resp.text

            # Expressões regulares para varrer players de vídeo comuns em EADs
            iframe_patterns = [
                r'https?://player\.pandavideo\.com\.br/[^\s"\'<>]+',
                r'https?://player\.vimeo\.com/video/\d+[^\s"\'<>]*',
                r'https?://iframe\.mediadelivery\.net/[^\s"\'<>]+',
                r'https?://[^\s"\'<>]+\.b-cdn\.net/[^\s"\'<>]+',
                r'https?://scripts\.converteai\.net/[^\s"\'<>]+',
                r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*',
                r'https?://www\.youtube\.com/embed/[^\s"\'<>]+',
                r'<iframe[^>]+src=["\']([^"\']+)["\']',
                r'data-src=["\']([^"\']+)["\']',
                r'data-video-url=["\']([^"\']+)["\']',
            ]

            found_urls = []
            for pattern in iframe_patterns:
                matches = re.findall(pattern, html, re.IGNORECASE)
                for m in matches:
                    url = m if isinstance(m, str) else m[0]
                    if url.startswith("//"):
                        url = "https:" + url
                    if url.startswith("http") and url not in found_urls:
                        found_urls.append(url)

            # Priorização de players de vídeo conhecidos
            for url in found_urls:
                if any(p in url.lower() for p in ["pandavideo", "vimeo", "b-cdn", "mediadelivery", "converteai", ".m3u8", "youtube"]):
                    print(f"🎯 [UniversoExtractor] Vídeo embutido encontrado: {url}")
                    return url, headers_extra

            # Se encontrou algum outro iframe de domínio externo
            for url in found_urls:
                if "universotecnico.com" not in url:
                    print(f"🎯 [UniversoExtractor] Iframe externo encontrado: {url}")
                    return url, headers_extra

        except Exception as e:
            print(f"⚠️ [UniversoExtractor] Erro ao extrair vídeo da aula: {e}")

        # Retorna a URL original caso nada seja encontrado
        return page_url, headers_extra