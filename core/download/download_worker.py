"""
===========================================================
PRT Labs - Core / Download
Class: PRTDownloadWorker, PRTCourseMapperWorker & UniversoExtractor

Description:
    Worker assíncrono para download de mídias com Sniffer de Rede,
    Bypass de Cookie WP, limpeza de caracteres ANSI e Extrator via JS.
===========================================================
"""

import os
import re
import time
from typing import Dict, Tuple, Optional, List
from PySide6.QtCore import QThread, Signal
import yt_dlp

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

try:
    import imageio_ffmpeg
    FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()
except ImportError:
    FFMPEG_PATH = None


def clean_ansi(text: str) -> str:
    """Remove códigos de cor e formatação ANSI do terminal."""
    if not text:
        return ""
    ansi_regex = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    cleaned = ansi_regex.sub('', str(text))
    return cleaned.replace('\r', '').strip()


class UniversoExtractor:
    """Extrator com suporte a cookies do WP e login inline."""

    def __init__(self, username: Optional[str] = None, password: Optional[str] = None) -> None:
        self.username = username
        self.password = password

    def extract_with_network_sniffer(self, page_url: str) -> Tuple[str, Dict[str, str]]:
        headers_extra = {
            "Referer": "https://universotecnico.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0 Safari/537.36"
        }

        captured_urls = []

        print("🤖 [UniversoExtractor] Abrindo janela do navegador...")
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,
                args=["--disable-blink-features=AutomationControlled"]
            )
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 720}
            )

            context.add_cookies([{
                "name": "wordpress_test_cookie",
                "value": "WP+Cookie+check",
                "domain": "universotecnico.com",
                "path": "/"
            }])

            page = context.new_page()

            def onRequest(request):
                url = request.url.lower()
                media_keywords = [
                    ".m3u8", ".mp4", "pandavideo.com.br", "player.vimeo.com", 
                    "b-cdn.net", "mediadelivery.net", "converteai.net", 
                    "kinescope", "cloudflarestream", "stream"
                ]
                if any(kw in url for kw in media_keywords):
                    if not any(ign in url for ign in [".jpg", ".png", ".css", ".js", "analytics", "favicon", ".svg", ".woff"]):
                        print(f"📡 [Sniffer de Rede] Fluxo detectado: {request.url}")
                        captured_urls.append(request.url)

            page.on("request", onRequest)

            try:
                if self.username and self.password:
                    print("🔑 [UniversoExtractor] Acessando tela de login principal...")
                    page.goto("https://universotecnico.com/wp-login.php", timeout=30000)
                    page.wait_for_load_state("domcontentloaded")
                    time.sleep(1)

                    user_field = page.locator("input[name='log'], #username, input[type='email']").first
                    pass_field = page.locator("input[name='pwd'], #password, input[type='password']").first
                    submit_btn = page.locator("#wp-submit, button[name='login'], input[type='submit']").first

                    if user_field.is_visible(timeout=3000):
                        user_field.fill(self.username)
                        pass_field.fill(self.password)
                        submit_btn.click()
                        print("✅ [UniversoExtractor] Form enviado. Aguardando...")
                        page.wait_for_timeout(3000)

                print(f"🌐 [UniversoExtractor] Carregando a aula: {page_url}")
                page.goto(page_url, timeout=35000)
                page.wait_for_load_state("domcontentloaded")
                time.sleep(2)

                entrar_btn = page.locator("a:has-text('Entrar'), button:has-text('Entrar')").first
                if entrar_btn.is_visible(timeout=2000):
                    print("🔑 [UniversoExtractor] Login primário pendente. Clicando em 'Entrar'...")
                    entrar_btn.click()
                    page.wait_for_timeout(2000)

                    modal_user = page.locator("input[name='log'], #username, input[type='email']").first
                    modal_pass = page.locator("input[name='pwd'], #password, input[type='password']").first
                    modal_sub = page.locator("#wp-submit, button[name='login'], input[type='submit']").first

                    if modal_user.is_visible(timeout=3000):
                        modal_user.fill(self.username)
                        modal_pass.fill(self.password)
                        modal_sub.click()
                        page.wait_for_timeout(4000)
                        page.goto(page_url, timeout=35000)
                        page.wait_for_load_state("domcontentloaded")
                        time.sleep(2)

                page.evaluate("window.scrollTo(0, document.body.scrollHeight / 3)")
                play_selectors = ["iframe", "video", ".vjs-big-play-button", "button", "div[class*='player']"]
                for selector in play_selectors:
                    try:
                        elem = page.locator(selector).first
                        if elem.is_visible():
                            elem.click(timeout=1500)
                            break
                    except Exception:
                        pass

                for _ in range(8):
                    if captured_urls:
                        break
                    time.sleep(1)

                browser.close()

                if captured_urls:
                    for u in captured_urls:
                        if ".m3u8" in u or "pandavideo" in u or "vimeo" in u or "b-cdn" in u:
                            print(f"🎯 [UniversoExtractor] Vídeo principal identificado: {u}")
                            return u, headers_extra
                    return captured_urls[0], headers_extra

            except Exception as e:
                print(f"⚠️ [UniversoExtractor] Erro na automação: {e}")
                try:
                    browser.close()
                except Exception:
                    pass

        return page_url, headers_extra

    def extract_video_url(self, page_url: str) -> Tuple[str, Dict[str, str]]:
        if HAS_PLAYWRIGHT:
            return self.extract_with_network_sniffer(page_url)
        else:
            return page_url, {"Referer": "https://universotecnico.com/"}


class UniversoCourseMapper:
    """Mapeador de cursos do Universo Técnico usando Playwright."""

    def __init__(self, username: str = None, password: str = None):
        self.username = username
        self.password = password

    def map_course(self, url: str) -> dict:
        from playwright.sync_api import sync_playwright

        lessons_found = []
        course_title = ""

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()

            # Realiza login se as credenciais forem fornecidas
            if self.username and self.password:
                try:
                    page.goto("https://universotecnico.com/minha-conta/", timeout=60000)
                    page.fill("input[name='username'], input[type='text']", self.username)
                    page.fill("input[name='password'], input[type='password']", self.password)
                    page.click("button[type='submit'], input[type='submit']")
                    page.wait_for_timeout(3000)
                except Exception as e:
                    print(f"[Mapper] Aviso no login: {e}")

            # Acessa a URL do curso
            page.goto(url, timeout=60000)
            page.wait_for_timeout(3000)

            # 🎯 Extração Automática do Nome do Curso (Elemento Amarelo)
            try:
                for selector in ["h1.entry-title", "h1.course-title", "h1", ".ld-course-title", "h2.entry-title"]:
                    if page.locator(selector).is_visible():
                        raw_title = page.locator(selector).first.inner_text().strip()
                        if raw_title:
                            # Trata títulos no formato "Nome do Curso por Autor"
                            course_title = raw_title.split("\n")[0].split(" por ")[0].strip()
                            break
                if not course_title:
                    course_title = page.title().split("-")[0].split("|")[0].strip()
            except Exception:
                course_title = ""

            # Extração de Lições/Aulas na página
            lesson_elements = page.locator("a[href*='/licoes/'], a[href*='/lessons/'], .ld-item-title").all()
            
            for idx, el in enumerate(lesson_elements, 1):
                title = el.inner_text().strip()
                href = el.get_attribute("href")
                if href and title:
                    lessons_found.append({
                        "index": idx,
                        "title": title,
                        "url": href,
                        "module": "Módulo 1",
                        "course_title": course_title or "Curso Mapeado"
                    })

            browser.close()

        return {
            "course_title": course_title or "Curso Mapeado",
            "lessons": lessons_found
        }

class PRTCourseMapperWorker(QThread):
    """Thread em segundo plano para mapear todas as aulas do curso."""

    course_mapped = Signal(list)
    status_changed = Signal(str)
    mapping_error = Signal(str)

    def __init__(
        self,
        course_url: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        parent=None
    ) -> None:
        super().__init__(parent)
        self.course_url = course_url
        self.username = username
        self.password = password

    def run(self) -> None:
        self.status_changed.emit("Mapeando grade do curso e aulas via JS...")
        try:
            mapper = UniversoCourseMapper(username=self.username, password=self.password)
            lessons = mapper.map_course(self.course_url)

            if lessons:
                self.course_mapped.emit(lessons)
                self.status_changed.emit(f"Sucesso! {len(lessons)} aulas encontradas na plataforma.")
            else:
                self.mapping_error.emit("Nenhuma aula foi encontrada. Verifique as credenciais de acesso.")
        except Exception as e:
            self.mapping_error.emit(f"Erro no mapeamento: {clean_ansi(str(e))}")


class PRTDownloadWorker(QThread):
    """Worker de download executado em thread separada com limpeza de caracteres."""

    progress_changed = Signal(dict)
    status_changed = Signal(str, str)
    download_finished = Signal(str)
    download_error = Signal(str)

    def __init__(
        self,
        media_url: str,
        output_path: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        course_name: Optional[str] = None,
        module_index: Optional[int] = None,
        module_name: Optional[str] = None,
        lesson_index: Optional[int] = None,
        lesson_name: Optional[str] = None,
        parent=None
    ) -> None:
        super().__init__(parent)
        self.media_url = media_url
        self.output_path = output_path
        self.username = username
        self.password = password

        self.course_name = course_name
        self.module_index = module_index
        self.module_name = module_name
        self.lesson_index = lesson_index
        self.lesson_name = lesson_name
        
        self._is_cancelled = False

    @staticmethod
    def _sanitize_name(name: str) -> str:
        if not name:
            return ""
        return re.sub(r'[\\/*?:"<>|]', "", name).strip()

    def _build_output_template(self) -> str:
        target_dir = self.output_path

        if self.course_name:
            target_dir = os.path.join(target_dir, self._sanitize_name(self.course_name))

        if self.module_name:
            if self.module_index is not None:
                mod_folder = f"{self.module_index:02d} - {self._sanitize_name(self.module_name)}"
            else:
                mod_folder = self._sanitize_name(self.module_name)
            target_dir = os.path.join(target_dir, mod_folder)

        os.makedirs(target_dir, exist_ok=True)

        if self.lesson_name:
            clean_lesson = self._sanitize_name(self.lesson_name)
            if self.lesson_index is not None:
                file_tmpl = f"{self.lesson_index:03d} {clean_lesson}.%(ext)s"
            else:
                file_tmpl = f"{clean_lesson}.%(ext)s"
        else:
            if self.lesson_index is not None:
                file_tmpl = f"{self.lesson_index:03d} %(title)s.%(ext)s"
            else:
                file_tmpl = "%(title)s.%(ext)s"

        return os.path.join(target_dir, file_tmpl)

    def run(self) -> None:
        self.status_changed.emit("DOWNLOADING", "Analisando fonte da mídia...")

        target_url = self.media_url
        custom_headers = {}

        if "universotecnico.com" in self.media_url.lower():
            if not HAS_PLAYWRIGHT:
                self.download_error.emit("Bibliotecas do navegador ausentes. Execute: pip install playwright")
                return

            self.status_changed.emit("DOWNLOADING", "Abrindo navegador para extrair sinal de vídeo...")
            extractor = UniversoExtractor(username=self.username, password=self.password)
            target_url, custom_headers = extractor.extract_video_url(self.media_url)

            if "universotecnico.com" in target_url.lower():
                self.download_error.emit(
                    "Não foi possível capturar o vídeo da página.\n"
                    "Verifique na janela do navegador se o login foi efetuado corretamente."
                )
                return

        out_template = self._build_output_template()

        ydl_opts = {
            "outtmpl": out_template,
            "progress_hooks": [self._yt_dlp_hook],
            "quiet": True,
            "no_warnings": True,
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
        }

        if FFMPEG_PATH:
            ydl_opts["ffmpeg_location"] = FFMPEG_PATH

        if custom_headers:
            ydl_opts["http_headers"] = custom_headers

        try:
            self.status_changed.emit("DOWNLOADING", "Baixando e unindo faixas de vídeo em MP4...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(target_url, download=True)
                filename = ydl.prepare_filename(info)

                base_name, _ = os.path.splitext(filename)
                final_file = (
                    f"{base_name}.mp4"
                    if os.path.exists(f"{base_name}.mp4")
                    else filename
                )

                if not self._is_cancelled:
                    self.status_changed.emit("COMPLETED", "Download concluído com sucesso!")
                    self.download_finished.emit(final_file)

        except Exception as e:
            if not self._is_cancelled:
                err_msg = clean_ansi(str(e))
                print(f"❌ [PRT Downloader Error]: {err_msg}")
                self.status_changed.emit("ERROR", err_msg)
                self.download_error.emit(err_msg)

    def _yt_dlp_hook(self, d: dict) -> None:
        if self._is_cancelled:
            raise Exception("Download cancelado pelo usuário.")

        if d.get("status") == "downloading":
            total_bytes = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            downloaded_bytes = d.get("downloaded_bytes") or 0

            percent = (
                (downloaded_bytes / total_bytes * 100) if total_bytes > 0 else 0.0
            )
            speed = clean_ansi(d.get("_speed_str", "N/A"))
            eta = clean_ansi(d.get("_eta_str", "N/A"))

            self.progress_changed.emit(
                {
                    "percent": percent,
                    "speed": speed,
                    "eta": eta,
                    "downloaded_bytes": downloaded_bytes,
                    "total_bytes": total_bytes,
                }
            )

    def cancel(self) -> None:
        self._is_cancelled = True
        self.status_changed.emit("CANCELLED", "Download cancelado.")