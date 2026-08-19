"""
===========================================================
PRT Labs - Core / Universo Técnico & Course Download Worker
File: core/download/universo_worker.py
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
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

try:
    import imageio_ffmpeg
    FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()
except ImportError:
    FFMPEG_PATH = None


class UniversoCourseMapper:
    """Mapeador de Cursos da Área de Membros."""

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
        lessons = []
        course_title = "Curso Extraído"
        cookie_string = ""
        cookies_list = []

        if not sync_playwright:
            print("[Mapper] Erro: Playwright não instalado.")
            return {"course_title": course_title, "lessons": lessons, "cookie_string": cookie_string, "cookies_list": cookies_list}

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            if self.username and self.password:
                try:
                    print("🔑 [Mapper] Acessando página de login...")
                    parsed = urllib.parse.urlparse(url)
                    login_url = f"{parsed.scheme}://{parsed.netloc}/wp-login.php"
                    page.goto(login_url, timeout=60000)
                    page.wait_for_load_state("domcontentloaded")
                    
                    user_input = page.locator("input[name='log'], #user_login, input[name='username'], input[type='email']").first
                    pass_input = page.locator("input[name='pwd'], #user_pass, input[name='password'], input[type='password']").first
                    submit_btn = page.locator("#wp-submit, input[type='submit'], button[type='submit'], input[name='login']").first

                    if user_input.is_visible():
                        user_input.click()
                        user_input.fill("")
                        user_input.type(self.username, delay=50)

                        pass_input.click()
                        pass_input.fill("")
                        pass_input.type(self.password, delay=50)

                        submit_btn.click()
                        page.wait_for_load_state("domcontentloaded", timeout=20000)
                        page.wait_for_timeout(4000)
                except Exception as e:
                    print(f"[Mapper] Aviso no login: {e}")

            print(f"🌐 [Mapper] Acessando curso: {url}")
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
            current_module_idx = 0
            
            IGNORE_TITLES = {
                "AULAS", "AULA", "LESSONS", "LESSON", "CONCLUÍDO", "CONCLUIDO", 
                "COMPLETED", "CONTEÚDO", "CONTEUDO", "TOPICS", "TÓPICOS"
            }

            for el in elements:
                try:
                    tag_name = el.evaluate("el => el.tagName").lower()
                    classes = el.get_attribute("class") or ""
                    
                    if tag_name in ['h2', 'h3'] or 'heading' in classes or 'title' in classes:
                        raw_text = el.inner_text().strip()
                        first_line = raw_text.split("\n")[0].strip()
                        cleaned_title = re.sub(r'(?i)\s*(concluído|concluido|completed)\s*$', '', first_line).strip()
                        
                        if cleaned_title.upper() in IGNORE_TITLES:
                            continue

                        if (
                            cleaned_title 
                            and len(cleaned_title) > 2 
                            and "curso" not in cleaned_title.lower() 
                            and tag_name != 'a'
                        ):
                            if cleaned_title != current_module_name:
                                current_module_name = cleaned_title
                                if current_module_idx == 0:
                                    current_module_idx = 1
                                else:
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
                                    "module": current_module_name if current_module_name else "Módulo 1",
                                    "module_index": max(1, current_module_idx),
                                    "course_title": course_title
                                })
                except Exception:
                    continue

            cookies_list = context.cookies()
            cookie_string = "; ".join([f"{c['name']}={c['value']}" for c in cookies_list])

            browser.close()

        return {
            "course_title": course_title,
            "lessons": lessons,
            "cookie_string": cookie_string,
            "cookies_list": cookies_list
        }


class UniversoDownloadWorker(QThread):
    """Worker isolado para Cursos EAD."""

    progress_changed = Signal(dict)
    status_changed = Signal(str, str)
    download_finished = Signal(str)
    download_error = Signal(str)

    def __init__(
        self,
        media_url: str,
        output_path: str = "",
        media_type: str = "video",
        quality: str = "best",
        cookie_string: str = "",
        cookies_list: list = None,
        course_name: str = "Curso",
        module_name: str = "Módulo 1",
        module_index: int = 1,
        lesson_index: int = 1,
        lesson_name: str = "Aula",
        username: str = "",
        password: str = "",
        parent=None,
        **kwargs
    ):
        super().__init__(parent)
        self.media_url = media_url or ""
        self.output_path = output_path or ""
        self.cookie_string = cookie_string or ""
        self.cookies_list = cookies_list or []
        self.course_name = course_name or "Curso"
        self.module_name = module_name or "Módulo 1"
        
        # Tratamento seguro contra valores None ou inválidos
        try:
            self.module_index = int(module_index) if module_index is not None else 1
        except (ValueError, TypeError):
            self.module_index = 1

        try:
            self.lesson_index = int(lesson_index) if lesson_index is not None else 1
        except (ValueError, TypeError):
            self.lesson_index = 1

        self.lesson_name = lesson_name or "Aula"
        self.username = username or ""
        self.password = password or ""
        self.captured_video_url = None

    def run(self):
        try:
            mod_idx = self.module_index
            les_idx = self.lesson_index

            mod_name_str = self._sanitize(self.module_name)
            lesson_name_str = self._sanitize(self.lesson_name)
            course_name_str = self._sanitize(self.course_name)

            safe_mod_title = f"{mod_idx:02d} - {mod_name_str}"
            target_dir = os.path.join(self.output_path, course_name_str, safe_mod_title)
            os.makedirs(target_dir, exist_ok=True)

            safe_lesson_title = f"{les_idx:02d} - {lesson_name_str}"
            final_filepath = os.path.join(target_dir, f"{safe_lesson_title}.mp4")

            self.status_changed.emit("extracting", f"🔍 Inspecionando aula: {self.media_url}...")

            real_video_url = None
            self.captured_video_url = None

            def _on_request(request):
                req_url = request.url
                if not req_url.endswith(".js") and "player.js" not in req_url:
                    if any(ext in req_url for ext in [".m3u8", ".mpd", "player.vimeo.com/video/", "pandavideo.com", "vidalytics.com", "vturb.com"]):
                        if not self.captured_video_url:
                            print(f"📡 [Course Intercept] Stream detectado: {req_url}")
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

                        print(f"🌐 [Universo Worker] Navegando até a aula: {self.media_url}")
                        page.goto(self.media_url, timeout=60000)
                        page.wait_for_load_state("domcontentloaded")
                        page.wait_for_timeout(3000)

                        user = self.username
                        passw = self.password

                        sem_acesso = page.locator("text='VOCÊ NÃO TEM ACESSO A ESTA AULA'")
                        btn_entrar = page.locator("a:has-text('Entrar'), button:has-text('Entrar')")

                        needs_login = False
                        try:
                            if sem_acesso.is_visible() or btn_entrar.is_visible() or "meus-cursos" in page.url or "wp-login" in page.url:
                                needs_login = True
                        except Exception:
                            pass

                        if needs_login:
                            print("🔑 [Universo Worker] Efetuando login...")
                            if btn_entrar.is_visible() and "meus-cursos" not in page.url and "wp-login" not in page.url:
                                try:
                                    btn_entrar.first.click()
                                    page.wait_for_load_state("domcontentloaded")
                                    page.wait_for_timeout(2000)
                                except Exception:
                                    pass

                            if user and passw:
                                user_input = page.locator("input[name='username'], input[name='log'], #user_login").first
                                pass_input = page.locator("input[name='password'], input[name='pwd'], #user_pass").first
                                submit_btn = page.locator("input[name='login'], button[name='login'], #wp-submit, input[type='submit']").first

                                try:
                                    user_input.wait_for(state="visible", timeout=5000)
                                    if user_input.is_visible():
                                        user_input.click()
                                        user_input.fill("")
                                        user_input.type(user, delay=50)

                                        pass_input.click()
                                        pass_input.fill("")
                                        pass_input.type(passw, delay=50)

                                        page.wait_for_timeout(1000)
                                        submit_btn.click()

                                        page.wait_for_load_state("domcontentloaded")
                                        page.wait_for_timeout(4000)
                                except Exception as err:
                                    print(f"⚠️ Erro no login: {err}")

                            page.goto(self.media_url, timeout=60000)
                            page.wait_for_load_state("domcontentloaded")
                            page.wait_for_timeout(4000)

                            self.cookies_list = context.cookies()
                            self.cookie_string = "; ".join([f"{c['name']}={c['value']}" for c in self.cookies_list])

                        for iframe in page.locator("iframe").all():
                            try:
                                src = iframe.get_attribute("src") or ""
                                if any(domain in src for domain in ["vimeo.com", "youtube.com", "pandavideo", "vturb"]):
                                    if not src.endswith(".js"):
                                        real_video_url = src
                                        break
                            except Exception:
                                continue

                        if not real_video_url:
                            for frame in page.frames:
                                frame_url = frame.url
                                if any(domain in frame_url for domain in ["vimeo.com/video/", "youtube.com/embed/"]):
                                    if not frame_url.endswith(".js"):
                                        real_video_url = frame_url
                                        break

                        if not real_video_url and self.captured_video_url:
                            real_video_url = self.captured_video_url

                        if not real_video_url:
                            html_content = page.content()
                            vimeo_match = re.search(r'player\.vimeo\.com/video/(\d+)', html_content) or re.search(r'vimeo\.com/(\d+)', html_content)
                            if vimeo_match:
                                real_video_url = f"https://player.vimeo.com/video/{vimeo_match.group(1)}"

                        browser.close()
                except Exception as e:
                    print(f"⚠️ [Universo Worker] Erro na inspeção: {e}")

            if not real_video_url:
                print(f"⚠️ Aula sem vídeo pulada: {safe_lesson_title}")
                self.status_changed.emit("finished", f"📄 Aula sem vídeo pulada: {safe_lesson_title}")
                return

            if real_video_url.startswith("//"):
                real_video_url = "https:" + real_video_url

            self.status_changed.emit("downloading", f"⬇️ Baixando aula: {safe_lesson_title}...")

            if yt_dlp:
                out_template = os.path.join(target_dir, f"{safe_lesson_title}.%(ext)s")

                http_headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                    'Referer': self.media_url
                }

                if self.cookie_string:
                    http_headers['Cookie'] = self.cookie_string

                ydl_opts = {
                    'outtmpl': out_template,
                    'format': 'bestvideo+bestaudio/best',
                    'progress_hooks': [self._ydl_hook],
                    'quiet': False,
                    'no_warnings': True,
                    'no_color': True,
                    'http_headers': http_headers
                }

                if FFMPEG_PATH:
                    ydl_opts['ffmpeg_location'] = FFMPEG_PATH

                print(f"🚀 [Universo Worker] Baixando stream: {real_video_url}")
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([real_video_url])

                if not os.path.exists(final_filepath):
                    base_path = os.path.splitext(final_filepath)[0]
                    for ext in ['.mp4', '.mkv', '.webm', '.ts']:
                        if os.path.exists(base_path + ext):
                            final_filepath = base_path + ext
                            break

            # Atualiza visualmente para 100% e marca como Concluído
            self.progress_changed.emit({"percent": 100, "speed": "0 B/s", "eta": "00:00"})
            self.status_changed.emit("finished", "Concluído")
            self.download_finished.emit(final_filepath)

        except Exception as e:
            self.download_error.emit(f"Erro ao baixar {self.lesson_name}: {str(e)}")

    def _ydl_hook(self, d):
        status = d.get('status')
        if status == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            downloaded = d.get('downloaded_bytes', 0)
            percent = (downloaded / total * 100) if total > 0 else 0
            
            if percent >= 99.0:
                percent = 99.0
                self.status_changed.emit("processing", "⚡ Mesclando áudio e vídeo...")

            speed = re.sub(r'\x1b\[[0-9;]*m', '', str(d.get('_speed_str', '0 B/s'))).strip()
            eta = re.sub(r'\x1b\[[0-9;]*m', '', str(d.get('_eta_str', '--:--'))).strip()
            self.progress_changed.emit({"percent": percent, "speed": speed, "eta": eta})
            
        elif status == 'finished':
            self.status_changed.emit("processing", "⚡ Finalizando e salvando arquivo...")

    def _sanitize(self, text: str) -> str:
        if not text:
            return "Midia"
        text = html.unescape(str(text))
        sanitized = re.sub(r'[\\/*?:"<>|]', "", text).strip()
        return sanitized if sanitized else "Midia"