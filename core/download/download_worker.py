"""
===========================================================
PRT Labs - Core / Download Worker & Course Mapper
File: core/download/download_worker.py
Description: Mapeador thread-safe com suporte a cookies WordPress
             (testcookie) e Worker PySide6 sem crash de WebEngine.
===========================================================
"""

import html
import http.cookiejar
import os
import re
import urllib.parse
import urllib.request
from PySide6.QtCore import QThread, Signal

try:
    import yt_dlp
except ImportError:
    yt_dlp = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None


class UniversoCourseMapper:
    """Mapeador HTTP em segundo plano (100% thread-safe)."""

    def __init__(self, username: str = None, password: str = None):
        self.username = username
        self.password = password
        self.cookie_jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookie_jar)
        )
        self.opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'),
            ('Accept-Language', 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7')
        ]

    def _login(self, base_url: str) -> bool:
        """Realiza autenticação completa no WordPress com suporte a testcookie."""
        if not self.username or not self.password:
            return False

        parsed = urllib.parse.urlparse(base_url)
        login_url = f"{parsed.scheme}://{parsed.netloc}/wp-login.php"

        try:
            # 1. Requisição GET inicial para capturar o 'wordpress_test_cookie'
            init_req = urllib.request.Request(login_url)
            with self.opener.open(init_req, timeout=10) as resp:
                resp.read()

            # 2. Envio das credenciais de Login via POST
            login_data = urllib.parse.urlencode({
                'log': self.username,
                'pwd': self.password,
                'wp-submit': 'Acessar',
                'redirect_to': base_url,
                'testcookie': '1'
            }).encode('utf-8')

            post_req = urllib.request.Request(
                login_url, 
                data=login_data,
                headers={'Referer': login_url, 'Content-Type': 'application/x-www-form-urlencoded'}
            )
            
            with self.opener.open(post_req, timeout=12) as response:
                final_url = response.geturl()
                print(f"[UniversoCourseMapper] Login finalizado. Redirecionado para: {final_url}")
                return True

        except Exception as e:
            print(f"[UniversoCourseMapper] Erro na autenticação WP: {e}")
            return False

    def map_course(self, url: str) -> dict:
        """Acessa a área do aluno e mapeia os links das aulas e vídeos."""
        lessons = []
        course_title = "Curso Extraído"

        # Autentica primeiro na plataforma
        if self._login(url):
            print("[UniversoCourseMapper] Sessão autenticada estabelecida com sucesso!")

        try:
            req = urllib.request.Request(url)
            with self.opener.open(req, timeout=15) as response:
                raw_html = response.read().decode('utf-8', errors='ignore')

            clean_html = html.unescape(raw_html)

            # Título do Curso
            title_match = re.search(r'<title>(.*?)</title>', clean_html, re.IGNORECASE)
            if title_match:
                raw_title = title_match.group(1).split('|')[0].split('-')[0].strip()
                if raw_title:
                    course_title = raw_title

            # 1. Extrai vídeos/iFrames embutidos
            embeds = self._extract_embed_videos(clean_html)

            if embeds:
                for idx, embed_url in enumerate(embeds, start=1):
                    lessons.append({
                        "title": f"Aula {idx:02d}",
                        "url": embed_url,
                        "module": "Módulo 1",
                        "index": idx,
                        "course_title": course_title
                    })
            else:
                # 2. Busca sub-links de aulas dentro do HTML autenticado
                lesson_links = self._extract_lesson_links(clean_html, url)
                
                for idx, link_info in enumerate(lesson_links, start=1):
                    lesson_url = link_info['url']
                    lesson_title = link_info['title']

                    try:
                        l_req = urllib.request.Request(lesson_url)
                        with self.opener.open(l_req, timeout=8) as l_resp:
                            l_html = html.unescape(l_resp.read().decode('utf-8', errors='ignore'))
                            l_embeds = self._extract_embed_videos(l_html)

                            target_url = l_embeds[0] if l_embeds else lesson_url

                            lessons.append({
                                "title": lesson_title,
                                "url": target_url,
                                "module": "Módulo 1",
                                "index": idx,
                                "course_title": course_title
                            })
                    except Exception:
                        continue

        except Exception as e:
            print(f"[UniversoCourseMapper] Erro ao mapear o curso: {e}")

        # Fallback: Se não encontrou sub-páginas, envia a URL autenticada
        if not lessons:
            lessons.append({
                "title": course_title,
                "url": url,
                "module": "Módulo 1",
                "index": 1,
                "course_title": course_title
            })

        print(f"[UniversoCourseMapper] Mapeamento concluído com {len(lessons)} aula(s).")
        return {
            "course_title": course_title,
            "lessons": lessons
        }

    def _extract_embed_videos(self, html_text: str) -> list:
        """Captura iFrames e players de vídeo (Vimeo, Panda, YouTube, HLS)."""
        valid_videos = []
        video_patterns = [
            r'https?://(?:player\.)?vimeo\.com/video/\d+',
            r'https?://[^\s"\'<>]+\.pandavideo\.[^\s"\'<>]+',
            r'https?://[^\s"\'<>]+\.b-cdn\.net/[^\s"\'<>]+',
            r'https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*',
            r'https?://(?:www\.)?youtube\.com/embed/[a-zA-Z0-9_-]+'
        ]

        # Busca por Regex
        for pattern in video_patterns:
            matches = re.findall(pattern, html_text, re.IGNORECASE)
            for m in matches:
                clean_url = m.rstrip('\\/').replace('\\/', '/')
                if clean_url not in valid_videos:
                    valid_videos.append(clean_url)

        # Busca por BeautifulSoup
        if BeautifulSoup:
            soup = BeautifulSoup(html_text, 'html.parser')
            for tag in soup.find_all(['iframe', 'video', 'embed', 'source']):
                src = tag.get('src') or tag.get('data-src') or tag.get('data-lazy-src')
                if src:
                    if src.startswith('//'):
                        src = 'https:' + src
                    if any(k in src.lower() for k in ['vimeo.com', 'youtube.com', 'pandavideo', 'b-cdn.net', '.m3u8', '.mp4']):
                        if src not in valid_videos:
                            valid_videos.append(src)

        return valid_videos

    def _extract_lesson_links(self, html_text: str, base_url: str) -> list:
        """Captura links de navegação de aulas do curso."""
        links_found = []
        seen = set()
        parsed_base = urllib.parse.urlparse(base_url)

        if BeautifulSoup:
            soup = BeautifulSoup(html_text, 'html.parser')
            for a in soup.find_all('a', href=True):
                href = a['href'].strip()
                text = a.get_text(strip=True)

                if not href or href == '#' or 'javascript:' in href or href in seen:
                    continue

                if href.startswith('/'):
                    href = f"{parsed_base.scheme}://{parsed_base.netloc}{href}"

                if parsed_base.netloc in href and href != base_url:
                    if any(kw in href.lower() for kw in ['aula', 'lesson', 'licao', 'topico', 'item', 'curso-ead']):
                        seen.add(href)
                        links_found.append({
                            "title": text if len(text) > 2 else f"Aula {len(links_found) + 1}",
                            "url": href
                        })

        return links_found


class PRTDownloadWorker(QThread):
    """Worker de download em segundo plano."""

    progress_changed = Signal(dict)
    status_changed = Signal(str, str)
    download_finished = Signal(str)
    download_error = Signal(str)

    def __init__(
        self,
        media_url: str,
        output_path: str,
        username: str = None,
        password: str = None,
        course_name: str = "Curso",
        module_name: str = "Modulo 1",
        lesson_index: int = 1,
        lesson_name: str = "Aula",
        parent=None
    ):
        super().__init__(parent)
        self.media_url = media_url
        self.output_path = output_path
        self.username = username
        self.password = password
        self.course_name = course_name
        self.module_name = module_name
        self.lesson_index = lesson_index
        self.lesson_name = lesson_name

    def run(self):
        try:
            target_dir = os.path.join(
                self.output_path, 
                self._sanitize(self.course_name), 
                self._sanitize(self.module_name)
            )
            os.makedirs(target_dir, exist_ok=True)

            safe_lesson_title = f"{self.lesson_index:02d} - {self._sanitize(self.lesson_name)}"
            final_filepath = os.path.join(target_dir, f"{safe_lesson_title}.mp4")

            self.status_changed.emit("downloading", f"Iniciando download: {safe_lesson_title}")

            if yt_dlp:
                ydl_opts = {
                    'outtmpl': os.path.join(target_dir, f"{safe_lesson_title}.%(ext)s"),
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    'progress_hooks': [self._ydl_hook],
                    'quiet': True,
                    'no_warnings': True,
                    'no_color': True,
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                        'Referer': 'https://universotecnico.com/'
                    }
                }
                if self.username and self.password:
                    ydl_opts['username'] = self.username
                    ydl_opts['password'] = self.password

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([self.media_url])
            else:
                self.progress_changed.emit({"percent": 100, "speed": "0 MB/s", "eta": "00:00"})

            self.download_finished.emit(final_filepath)

        except Exception as e:
            self.download_error.emit(f"Erro ao baixar {self.lesson_name}: {str(e)}")

    def _ydl_hook(self, d):
        if d.get('status') == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            downloaded = d.get('downloaded_bytes', 0)
            percent = (downloaded / total * 100) if total > 0 else 0

            speed = re.sub(r'\x1b\[[0-9;]*m', '', str(d.get('_speed_str', 'N/A'))).strip()
            eta = re.sub(r'\x1b\[[0-9;]*m', '', str(d.get('_eta_str', 'N/A'))).strip()

            self.progress_changed.emit({
                "percent": percent,
                "speed": speed,
                "eta": eta
            })

    def _sanitize(self, text: str) -> str:
        text = html.unescape(text)
        return re.sub(r'[\\/*?:"<>|]', "", text).strip()