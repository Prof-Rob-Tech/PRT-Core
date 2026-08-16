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
            init_req = urllib.request.Request(login_url)
            with self.opener.open(init_req, timeout=10) as resp:
                resp.read()

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

        if not sync_playwright:
            print("[Mapper] Erro: Playwright não está instalado. Instale com 'pip install playwright'.")
            return {"course_title": course_title, "lessons": lessons}

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            # Realiza login se as credenciais forem fornecidas
            if self.username and self.password:
                try:
                    print("🔑 [Mapper] Acessando página de login principal...")
                    parsed = urllib.parse.urlparse(url)
                    login_url = f"{parsed.scheme}://{parsed.netloc}/wp-login.php"
                    page.goto(login_url, timeout=60000)
                    
                    page.fill("input[name='log'], #user_login, input[type='email'], input[type='text']", self.username)
                    page.fill("input[name='pwd'], #user_pass, input[type='password']", self.password)
                    page.click("#wp-submit, input[type='submit'], button[type='submit']")
                    
                    print("✅ [Mapper] Formulário enviado. Aguardando o site processar o login...")
                    page.wait_for_load_state("domcontentloaded", timeout=20000)
                    page.wait_for_timeout(4000) 
                except Exception as e:
                    print(f"[Mapper] Aviso no login: {e}")

            # Acessa a URL do curso
            print(f"🌐 [Mapper] Acessando página do curso: {url}")
            page.goto(url, timeout=60000)
            page.wait_for_load_state("domcontentloaded", timeout=15000)
            page.wait_for_timeout(3000) 

            # 🎯 Extração Automática do Nome do Curso
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

            print(f"📚 [Mapper] Título do curso detectado: {course_title}")
            print("🔍 [Mapper] Buscando módulos e aulas...")

            # 🎯 Extração Inteligente (Lendo a página de cima pra baixo)
            # Ele vai procurar Títulos (Módulos) e Links (Aulas)
            selectors = [
                "h2", "h3", ".ld-section-heading", ".module-title", ".section-title", # Possíveis títulos de módulo
                "a[href*='/licoes/']", "a[href*='/lessons/']", "a[href*='/aulas/']", "a[href*='/aula/']", "a.lesson-title" # Links de aulas
            ]
            
            elements = page.locator(", ".join(selectors)).all()
            
            seen_urls = set()
            current_module_name = "Módulo 1" # Padrão caso não ache título antes da primeira aula
            current_module_idx = 1
            
            for el in elements:
                try:
                    tag_name = el.evaluate("el => el.tagName").lower()
                    classes = el.get_attribute("class") or ""
                    
                    # Se for um Header ou Div de título, atualizamos o módulo atual
                    if tag_name in ['h2', 'h3'] or 'heading' in classes or 'title' in classes:
                        text = el.inner_text().strip()
                        # Ignora textos muito curtos ou inúteis
                        if text and len(text) > 3 and "curso" not in text.lower() and tag_name != 'a':
                            if text != current_module_name:
                                current_module_name = text
                                current_module_idx += 1
                                print(f"📁 [Mapper] Novo módulo detectado: {current_module_name}")
                        continue
                    
                    # Se for um Link (A), é uma aula
                    if tag_name == 'a':
                        title = el.inner_text().strip()
                        href = el.get_attribute("href")
                        
                        if href and title and href not in seen_urls:
                            if url in href or urllib.parse.urlparse(url).netloc in href: # Garante que é link do site
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

            browser.close()

        print(f"[UniversoCourseMapper] Mapeamento concluído com {len(lessons)} aula(s).")
        return {
            "course_title": course_title,
            "lessons": lessons
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
        username: str = None,
        password: str = None,
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
        self.username = username
        self.password = password
        self.course_name = course_name
        self.module_name = module_name
        self.module_index = module_index
        self.lesson_index = lesson_index
        self.lesson_name = lesson_name

    def run(self):
        try:
            # Constrói o nome da pasta do módulo com índice numérico (Ex: "01 - Introdução")
            safe_mod_title = f"{self.module_index:02d} - {self._sanitize(self.module_name)}"
            
            target_dir = os.path.join(
                self.output_path, 
                self._sanitize(self.course_name), 
                safe_mod_title
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
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                }
                
                # Ajusta para áudio se for selecionado
                if self.media_type == "audio":
                    ydl_opts['format'] = 'bestaudio/best'
                    ydl_opts['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]
                    final_filepath = os.path.join(target_dir, f"{safe_lesson_title}.mp3")

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