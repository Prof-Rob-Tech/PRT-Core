"""
===========================================================
PRT Labs - Core / Download Worker & Course Mapper
File: core/download/download_worker.py
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

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None


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
            ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'),
            ('Accept-Language', 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7')
        ]

    def map_course(self, url: str) -> dict:
        """Acessa a área do aluno e mapeia os links das aulas, vídeos e cookies."""
        lessons = []
        course_title = "Curso Extraído"
        cookie_string = ""
        cookies_list = []

        if not sync_playwright:
            print("[Mapper] Erro: Playwright não está instalado.")
            return {"course_title": course_title, "lessons": lessons, "cookie_string": cookie_string, "cookies_list": cookies_list}

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            if self.username and self.password:
                try:
                    print("🔑 [Mapper] Acessando página de login principal...")
                    parsed = urllib.parse.urlparse(url)
                    login_url = f"{parsed.scheme}://{parsed.netloc}/wp-login.php"
                    page.goto(login_url, timeout=60000)
                    
                    page.fill("input[name='log'], #user_login, input[type='email'], input[type='text']", self.username)
                    page.fill("input[name='pwd'], #user_pass, input[type='password']", self.password)
                    page.click("#wp-submit, input[type='submit'], button[type='submit']")
                    
                    print("✅ [Mapper] Formulário enviado. Aguardando...")
                    page.wait_for_load_state("domcontentloaded", timeout=20000)
                    page.wait_for_timeout(4000) 
                except Exception as e:
                    print(f"[Mapper] Aviso no login: {e}")

            print(f"🌐 [Mapper] Acessando página do curso: {url}")
            page.goto(url, timeout=60000)
            page.wait_for_load_state("domcontentloaded", timeout=15000)
            page.wait_for_timeout(3000) 

            try:
                for selector in ["h1.entry-title", "h1.course-title", "h1", ".ld-course-title", "h2.entry-title"]:
                    if page.locator(selector).is_visible():
                        raw_title = page.locator(selector).first.inner_text().strip()
                        if raw_title:
                            course_title = raw_title.split("\n")[0].split(" por ")[0].strip()
                            break
                if course_title == "Curso Extraído":
                    course_title = page.title().split("-")[0].split("|")[0].strip()
            except Exception:
                course_title = "Curso Extraído"

            selectors = [
                "h2", "h3", ".ld-section-heading", ".module-title", ".section-title", 
                "a[href*='/licoes/']", "a[href*='/lessons/']", "a[href*='/aulas/']", "a[href*='/aula/']", "a.lesson-title"
            ]
            
            elements = page.locator(", ".join(selectors)).all()
            seen_urls = set()
            current_module_name = "Módulo 1"
            current_module_idx = 1
            
            for el in elements:
                try:
                    tag_name = el.evaluate("el => el.tagName").lower()
                    classes = el.get_attribute("class") or ""
                    
                    if tag_name in ['h2', 'h3'] or 'heading' in classes or 'title' in classes:
                        text = el.inner_text().strip()
                        if text and len(text) > 3 and "curso" not in text.lower() and tag_name != 'a':
                            if text != current_module_name:
                                current_module_name = text
                                current_module_idx += 1
                        continue
                    
                    if tag_name == 'a':
                        title = el.inner_text().strip()
                        href = el.get_attribute("href")
                        
                        if href and title and href not in seen_urls:
                            if url in href or urllib.parse.urlparse(url).netloc in href:
                                seen_urls.add(href)
                                lessons.append({
                                    "index": len(lessons) + 1,
                                    "title": title,
                                    "url": href,
                                    "module": current_module_name,
                                    "module_index": current_module_idx,
                                    "course_title": course_title
                                })
                except Exception:
                    continue

            cookies_list = context.cookies()
            cookie_string = "; ".join([f"{c['name']}={c['value']}" for c in cookies_list])

            browser.close()

        print(f"[UniversoCourseMapper] Mapeamento concluído com {len(lessons)} aula(s).")
        return {
            "course_title": course_title,
            "lessons": lessons,
            "cookie_string": cookie_string,
            "cookies_list": cookies_list
        }


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
        media_type: str = "video",
        quality: str = "best",
        cookie_string: str = "",
        cookies_list: list = None,
        course_name: str = "Curso",
        module_name: str = "Módulo 1",
        module_index: int = 1,
        lesson_index: int = 1,
        lesson_name: str = "Aula",
        parent=None
    ):
        super().__init__(parent)
        self.media_url = media_url
        self.output_path = output_path
        self.media_type = media_type
        self.quality = quality
        self.cookie_string = cookie_string
        self.cookies_list = cookies_list or []
        self.course_name = course_name
        self.module_name = module_name
        self.module_index = module_index
        self.lesson_index = lesson_index
        self.lesson_name = lesson_name
        self.captured_video_url = None

    def run(self):
        try:
            safe_mod_title = f"{self.module_index:02d} - {self._sanitize(self.module_name)}"
            target_dir = os.path.join(
                self.output_path, 
                self._sanitize(self.course_name), 
                safe_mod_title
            )
            os.makedirs(target_dir, exist_ok=True)

            safe_lesson_title = f"{self.lesson_index:02d} - {self._sanitize(self.lesson_name)}"
            final_filepath = os.path.join(target_dir, f"{safe_lesson_title}.mp4")

            self.status_changed.emit("extracting", f"🔍 Inspecionando aula: {safe_lesson_title}...")
            
            real_video_url = None
            self.captured_video_url = None

            def _on_request(request):
                req_url = request.url
                # Filtra estritamente para pegar apenas MÍDIAS, ignorando scripts .js da API do Vimeo
                if not req_url.endswith(".js") and "player.js" not in req_url:
                    if any(ext in req_url for ext in [".m3u8", ".mpd", "pandavideo.com", "vidalytics.com", "vturb.com"]):
                        if not self.captured_video_url:
                            print(f"📡 [Network Intercept] Stream de vídeo detectado: {req_url}")
                            self.captured_video_url = req_url

            if sync_playwright:
                try:
                    with sync_playwright() as p:
                        browser = p.chromium.launch(headless=False)
                        context = browser.new_context()
                        
                        if self.cookies_list:
                            context.add_cookies(self.cookies_list)
                        
                        page = context.new_page()
                        page.on("request", _on_request)
                        
                        print(f"🌐 [Worker] Navegando até a aula: {self.media_url}")
                        page.goto(self.media_url, timeout=60000)
                        page.wait_for_load_state("domcontentloaded")
                        page.wait_for_timeout(3000)

                        # Se redirecionou para tela de login por perda de cookie, refaz o login na hora
                        if "wp-login.php" in page.url or page.locator("input[name='log']").is_visible():
                            print("🔑 [Worker] Sessão expirada. Autenticando novamente...")
                            parsed = urllib.parse.urlparse(self.media_url)
                            login_url = f"{parsed.scheme}://{parsed.netloc}/wp-login.php"
                            page.goto(login_url, timeout=30000)
                            
                            # Tenta pegar credenciais enviadas via parent se existirem
                            if hasattr(self.parent(), 'username') and self.parent().username:
                                page.fill("input[name='log']", self.parent().username)
                                page.fill("input[name='pwd']", self.parent().password)
                                page.click("#wp-submit")
                                page.wait_for_timeout(3000)
                                page.goto(self.media_url, timeout=60000)

                        # 1. Busca por IFRAME do Vimeo/YouTube/Panda (Método mais confiável)
                        iframes = page.locator("iframe").all()
                        for iframe in iframes:
                            src = iframe.get_attribute("src") or ""
                            if "vimeo.com" in src or "youtube.com" in src or "panda" in src:
                                real_video_url = src
                                print(f"🎯 [IFrame Hunter] Vídeo localizado via IFrame: {real_video_url}")
                                break

                        # 2. Busca por Frames aninhados
                        if not real_video_url:
                            for frame in page.frames:
                                frame_url = frame.url
                                if any(p in frame_url for p in ["vimeo.com/video/", "youtube.com/embed/"]):
                                    if not frame_url.endswith(".js"):
                                        real_video_url = frame_url
                                        print(f"🎯 [Frame Hunter] Vídeo localizado via Frame: {real_video_url}")
                                        break

                        # 3. Usa o Stream detectado pela rede se os frames falharem
                        if not real_video_url and self.captured_video_url:
                            real_video_url = self.captured_video_url
                            print(f"🎯 [Network Hunter] Usando stream interceptado: {real_video_url}")

                        # 4. Procura por Vimeo ID diretamente no HTML
                        if not real_video_url:
                            html_content = page.content()
                            vimeo_match = re.search(r'player\.vimeo\.com/video/(\d+)', html_content) or re.search(r'vimeo\.com/(\d+)', html_content)
                            if vimeo_match:
                                real_video_url = f"https://player.vimeo.com/video/{vimeo_match.group(1)}"
                                print(f"🎯 [HTML Hunter] Vimeo ID localizado: {real_video_url}")

                        browser.close()
                except Exception as e:
                    print(f"⚠️ [Worker] Erro na inspeção: {e}")

            if not real_video_url:
                print("⚠️ [Worker] Esta aula não possui player de vídeo (ou é página de texto/PDF). Pulando...")
                self.status_changed.emit("finished", f"📄 Aula sem vídeo pulada: {safe_lesson_title}")
                return

            self.status_changed.emit("downloading", f"⬇️ Baixando vídeo: {safe_lesson_title}")

            if yt_dlp:
                ydl_opts = {
                    'outtmpl': os.path.join(target_dir, f"{safe_lesson_title}.%(ext)s"),
                    'format': 'bestvideo+bestaudio/best', 
                    'progress_hooks': [self._ydl_hook],
                    'quiet': False,
                    'no_warnings': True,
                    'no_color': True,
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Referer': self.media_url 
                    }
                }
                
                if hasattr(self, 'cookie_string') and self.cookie_string:
                    ydl_opts['http_headers']['Cookie'] = self.cookie_string

                print(f"🚀 [yt-dlp] Iniciando download do link: {real_video_url}")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([real_video_url]) 
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
            self.progress_changed.emit({"percent": percent, "speed": speed, "eta": eta})

    def _sanitize(self, text: str) -> str:
        text = html.unescape(text)
        return re.sub(r'[\\/*?:"<>|]', "", text).strip()