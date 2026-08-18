"""
===========================================================
PRT Labs - UI / Pages
Class: ConnectorPage
Description: Template genérico e adaptável para conectores com suporte a
             seletor de qualidade, Login/Senha, detecção automática do
             nome do curso, criação de estrutura de pastas e downloads.
===========================================================
"""

import inspect
import os
import traceback
from PySide6.QtCore import Qt, QThread, Signal, Slot
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

try:
    from core.download.download_worker import PRTDownloadWorker, UniversoCourseMapper
except ImportError:
    try:
        from download_worker import PRTDownloadWorker, UniversoCourseMapper  # type: ignore
    except ImportError:
        PRTDownloadWorker = None
        UniversoCourseMapper = None


class CourseMapThread(QThread):
    """Thread em segundo plano para mapeamento com tratamento rigoroso de erros e extração do título do curso."""
    finished_signal = Signal(object)  # Aceita dict ou list
    error_signal = Signal(str)

    def __init__(self, course_url, username, password, parent=None):
        super().__init__(parent)
        self.course_url = course_url
        self.username = username
        self.password = password

    def run(self):
        try:
            if not UniversoCourseMapper:
                self.error_signal.emit("Módulo 'UniversoCourseMapper' não encontrado em 'download_worker.py'.")
                return

            mapper = UniversoCourseMapper(username=self.username, password=self.password)
            result = mapper.map_course(self.course_url)

            if not result:
                self.error_signal.emit("Nenhuma aula foi encontrada. Verifique se o link ou login estão corretos.")
                return

            self.finished_signal.emit(result)

        except Exception as e:
            traceback.print_exc()
            self.error_signal.emit(f"Falha no Playwright: {str(e)}")


class ConnectorPage(QWidget):
    """Página de Conector Genérica adaptável aos temas do PRT Nexus."""

    def __init__(self, platform_key: str = "conector", connector_name: str = "Conector", parent=None) -> None:
        super().__init__(parent)
        self.platform_key = platform_key.lower()
        self.connector_name = connector_name.title() if connector_name else "Conector"
        self.active_worker = None
        self.map_thread = None
        self.lessons_queue = []
        self.current_lesson_index = 0
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # 1. Cabeçalho
        title_layout = QVBoxLayout()
        title_layout.setSpacing(4)

        lbl_title = QLabel(f"Conector {self.connector_name}")
        lbl_title.setStyleSheet("font-size: 20px; font-weight: bold; color: #FFFFFF;")

        lbl_subtitle = QLabel(f"Capture, extraia e gerencie conteúdos diretamente do {self.connector_name}.")
        lbl_subtitle.setStyleSheet("color: #8E8E93; font-size: 13px;")

        title_layout.addWidget(lbl_title)
        title_layout.addWidget(lbl_subtitle)
        layout.addLayout(title_layout)

        # 2. Card de Captura e Configurações
        card_capture = QFrame()
        card_capture.setObjectName("cardFrame")
        card_capture.setStyleSheet("""
            QFrame#cardFrame {
                background-color: #18181B;
                border: 1px solid #27272A;
                border-radius: 8px;
            }
            QLabel { color: #FAFAFA; }
            QLineEdit, QComboBox, QSpinBox {
                background-color: #09090B;
                border: 1px solid #27272A;
                border-radius: 6px;
                color: #FFFFFF;
                padding: 6px 10px;
            }
            QPushButton {
                background-color: #6366F1;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 7px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4F46E5;
            }
            QPushButton:disabled {
                background-color: #3F3F46;
                color: #71717A;
            }
            QPushButton#btnMap {
                background-color: #10B981;
            }
            QPushButton#btnMap:hover {
                background-color: #059669;
            }
        """)

        c_layout = QVBoxLayout(card_capture)
        c_layout.setContentsMargins(15, 15, 15, 15)
        c_layout.setSpacing(12)

        lbl_cap_title = QLabel(f"🔗 Capturar Mídia via URL - {self.connector_name}")
        lbl_cap_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        c_layout.addWidget(lbl_cap_title)

        # Linha URL + Formato/Qualidade + Botões
        input_layout = QHBoxLayout()
        self.txt_url = QLineEdit()
        self.txt_url.setPlaceholderText(f"Cole o link da aula ou curso do {self.connector_name} aqui (ex: https://...)")

        # Seletor de Qualidade
        self.combo_format = QComboBox()
        self.combo_format.addItems([
            "📹 Vídeo - Max Qualidade (MP4)",
            "📹 Vídeo - 1080p Full HD (MP4)",
            "📹 Vídeo - 720p HD (MP4)",
            "📹 Vídeo - 480p SD (MP4)",
            "🎵 Apenas Áudio (MP3)"
        ])

        self.btn_download = QPushButton("⬇️ Baixar Mídia")
        self.btn_download.setCursor(Qt.PointingHandCursor)
        self.btn_download.clicked.connect(self._start_download)

        self.btn_map_course = QPushButton("🗺️ Mapear e Baixar Curso")
        self.btn_map_course.setObjectName("btnMap")
        self.btn_map_course.setCursor(Qt.PointingHandCursor)
        self.btn_map_course.clicked.connect(self._start_course_mapping)

        input_layout.addWidget(self.txt_url, stretch=3)
        input_layout.addWidget(self.combo_format, stretch=1)
        input_layout.addWidget(self.btn_download)
        input_layout.addWidget(self.btn_map_course)
        c_layout.addLayout(input_layout)

        # Autenticação
        auth_group = QVBoxLayout()
        auth_lbl = QLabel(f"🔐 Autenticação / Conta {self.connector_name} (Necessário para áreas pagas):")
        auth_lbl.setStyleSheet("color: #A1A1AA; font-size: 12px; font-weight: bold; margin-top: 4px;")
        auth_group.addWidget(auth_lbl)

        row_auth = QHBoxLayout()
        self.txt_user = QLineEdit()
        self.txt_user.setPlaceholderText("E-mail / Usuário de Acesso")

        self.txt_pass = QLineEdit()
        self.txt_pass.setEchoMode(QLineEdit.Password)
        self.txt_pass.setPlaceholderText("Senha de Acesso")

        row_auth.addWidget(self.txt_user)
        row_auth.addWidget(self.txt_pass)
        auth_group.addLayout(row_auth)
        c_layout.addLayout(auth_group)

        # Organização de Pastas do Curso
        struct_group = QVBoxLayout()
        struct_lbl = QLabel("📁 Organização de Pastas do Curso (Detectado automaticamente ou personalize):")
        struct_lbl.setStyleSheet("color: #A1A1AA; font-size: 12px; font-weight: bold; margin-top: 4px;")
        struct_group.addWidget(struct_lbl)

        # Nome do Curso
        self.txt_course = QLineEdit()
        self.txt_course.setPlaceholderText("Nome do Curso (Será preenchido automaticamente ao mapear)")
        struct_group.addWidget(self.txt_course)

        # Módulo e Aula em paralelo
        row_mod_les = QHBoxLayout()

        self.spin_module_idx = QSpinBox()
        self.spin_module_idx.setRange(1, 999)
        self.spin_module_idx.setPrefix("Mod ")
        self.spin_module_idx.setValue(1)

        self.txt_module_name = QLineEdit()
        self.txt_module_name.setPlaceholderText("Nome do Módulo (ex: Apresentação conteúdo Face ID 2.0)")

        self.spin_lesson_idx = QSpinBox()
        self.spin_lesson_idx.setRange(1, 9999)
        self.spin_lesson_idx.setPrefix("Aula ")
        self.spin_lesson_idx.setValue(1)

        self.txt_lesson_name = QLineEdit()
        self.txt_lesson_name.setPlaceholderText("Nome da Aula (ex: Apresentação - Curso Face ID)")

        row_mod_les.addWidget(self.spin_module_idx, stretch=1)
        row_mod_les.addWidget(self.txt_module_name, stretch=3)
        row_mod_les.addWidget(self.spin_lesson_idx, stretch=1)
        row_mod_les.addWidget(self.txt_lesson_name, stretch=3)

        struct_group.addLayout(row_mod_les)
        c_layout.addLayout(struct_group)

        # Pasta de Saída
        folder_layout = QHBoxLayout()
        default_folder = os.path.join(os.path.expanduser("~"), "Downloads", "PRT_Nexus")
        self.txt_folder = QLineEdit(default_folder)
        
        btn_folder = QPushButton("📁 Alterar Pasta")
        btn_folder.setCursor(Qt.PointingHandCursor)
        btn_folder.clicked.connect(self._select_folder)

        folder_layout.addWidget(self.txt_folder, stretch=4)
        folder_layout.addWidget(btn_folder, stretch=1)
        c_layout.addLayout(folder_layout)

        # Barra e Status de Progresso
        progress_layout = QVBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #09090B;
                border: 1px solid #27272A;
                border-radius: 6px;
                text-align: center;
                color: #FFFFFF;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #10B981;
                border-radius: 5px;
            }
        """)

        self.lbl_status = QLabel("Aguardando link de download...")
        self.lbl_status.setStyleSheet("color: #A1A1AA; font-size: 12px;")

        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.lbl_status)
        c_layout.addLayout(progress_layout)

        layout.addWidget(card_capture)

        # 3. Tabela de Mídias Concluídas (BLOCO ÚNICO SEM DUPLICAÇÕES)
        card_table = QFrame()
        card_table.setObjectName("cardFrame")
        card_table.setStyleSheet("""
            QFrame#cardFrame {
                background-color: #18181B;
                border: 1px solid #27272A;
                border-radius: 8px;
            }
            QLabel { color: #FAFAFA; }
            QTableWidget {
                background-color: #09090B;
                border: 1px solid #27272A;
                gridline-color: #27272A;
                color: #FFFFFF;
                border-radius: 6px;
            }
            QHeaderView::section {
                background-color: #18181B;
                color: #A1A1AA;
                padding: 6px;
                border: none;
                font-weight: bold;
            }
        """)
        t_layout = QVBoxLayout(card_table)
        t_layout.setContentsMargins(15, 15, 15, 15)

        lbl_tbl_title = QLabel(f"📦 Mídias Concluídas do {self.connector_name}")
        lbl_tbl_title.setStyleSheet("font-weight: bold; font-size: 13px; margin-bottom: 8px;")
        t_layout.addWidget(lbl_tbl_title)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["#", "Título / Nome do Arquivo", "Caminho Salvo", "Status"])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        self.table.setColumnWidth(0, 40)
        
        header.setSectionResizeMode(1, QHeaderView.Interactive)
        self.table.setColumnWidth(1, 260)
        
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        self.table.setColumnWidth(3, 100)

        self.table.setMinimumHeight(220)

        t_layout.addWidget(self.table)
        layout.addWidget(card_table, 1)

    def _create_worker(self, **kwargs):
        """Instancia PRTDownloadWorker repassando apenas os parâmetros suportados."""
        if not PRTDownloadWorker:
            return None

        try:
            sig = inspect.signature(PRTDownloadWorker.__init__)
            param_names = set(sig.parameters.keys())

            if "url" in param_names and "media_url" in kwargs:
                kwargs["url"] = kwargs["media_url"]
            if "output_dir" in param_names and "output_path" in kwargs:
                kwargs["output_dir"] = kwargs["output_path"]
            if "format" in param_names and "media_type" in kwargs:
                kwargs["format"] = kwargs["media_type"]

            filtered_kwargs = {k: v for k, v in kwargs.items() if k in param_names}
            return PRTDownloadWorker(**filtered_kwargs)
        except Exception:
            return PRTDownloadWorker(
                media_url=kwargs.get("media_url"),
                output_path=kwargs.get("output_path"),
                parent=self,
            )

    def _get_selected_quality_params(self):
        selected = self.combo_format.currentText()
        if "Áudio" in selected:
            return "audio", "best"
        elif "1080p" in selected:
            return "video", "1080p"
        elif "720p" in selected:
            return "video", "720p"
        elif "480p" in selected:
            return "video", "480p"
        else:
            return "video", "best"

    def _select_folder(self) -> None:
        chosen = QFileDialog.getExistingDirectory(self, "Selecione a Pasta de Destino", self.txt_folder.text())
        if chosen:
            self.txt_folder.setText(chosen)

    def _start_download(self) -> None:
        url = self.txt_url.text().strip()
        if not url:
            self.lbl_status.setText("⚠️ Digite ou cole uma URL válida antes de baixar.")
            return

        if not PRTDownloadWorker:
            self.lbl_status.setText("❌ Erro: O módulo 'download_worker' não foi encontrado.")
            return

        media_type, quality = self._get_selected_quality_params()
        user = self.txt_user.text().strip() or None
        pwd = self.txt_pass.text().strip() or None

        output_dir = self.txt_folder.text().strip()
        course = self.txt_course.text().strip() or None
        mod_idx = self.spin_module_idx.value() if self.txt_module_name.text().strip() else None
        mod_name = self.txt_module_name.text().strip() or None
        les_idx = self.spin_lesson_idx.value() if self.txt_lesson_name.text().strip() else None
        les_name = self.txt_lesson_name.text().strip() or None

        self.btn_download.setEnabled(False)
        self.btn_map_course.setEnabled(False)
        self.progress_bar.setValue(0)
        self.lbl_status.setText(f"🚀 Iniciando download ({quality})...")

        self.active_worker = self._create_worker(
            media_url=url,
            output_path=output_dir,
            media_type=media_type,
            quality=quality,
            username=user,
            password=pwd,
            course_name=course,
            module_index=mod_idx,
            module_name=mod_name,
            lesson_index=les_idx,
            lesson_name=les_name,
            parent=self
        )

        if not self.active_worker:
            self.lbl_status.setText("❌ Erro ao criar a tarefa de download.")
            self.btn_download.setEnabled(True)
            self.btn_map_course.setEnabled(True)
            return

        self.active_worker.progress_changed.connect(self._on_progress)
        self.active_worker.status_changed.connect(self._on_status)
        self.active_worker.download_finished.connect(self._on_finished)
        self.active_worker.download_error.connect(self._on_error)

        self.active_worker.start()

    def _start_course_mapping(self) -> None:
        url = self.txt_url.text().strip()
        if not url:
            self.lbl_status.setText("⚠️ Cole o link principal do curso para mapear.")
            return

        user = self.txt_user.text().strip() or None
        pwd = self.txt_pass.text().strip() or None

        self.btn_download.setEnabled(False)
        self.btn_map_course.setEnabled(False)
        self.progress_bar.setValue(0)
        self.lbl_status.setText("🗺️ Mapeando estrutura de aulas do curso com Playwright... Aguarde!")

        self.map_thread = CourseMapThread(course_url=url, username=user, password=pwd, parent=self)
        self.map_thread.finished_signal.connect(self._on_mapping_finished)
        self.map_thread.error_signal.connect(self._on_mapping_error)
        self.map_thread.start()

    @Slot(object)
    def _on_mapping_finished(self, result) -> None:
        course_title = ""
        lessons = []

        if isinstance(result, dict):
            lessons = result.get("lessons", [])
            course_title = result.get("course_title", "")
        elif isinstance(result, list):
            lessons = result
            if lessons and isinstance(lessons[0], dict):
                course_title = lessons[0].get("course_title") or lessons[0].get("course") or ""

        if course_title and not self.txt_course.text().strip():
            self.txt_course.setText(course_title)

        if not lessons:
            self.btn_download.setEnabled(True)
            self.btn_map_course.setEnabled(True)
            self.lbl_status.setText("⚠️ Nenhuma aula foi encontrada na página digitada.")
            return

        self.lessons_queue = lessons
        self.current_lesson_index = 0
        self.lbl_status.setText(f"✅ Mapeamento concluído! Total de {len(lessons)} aulas encontradas. Iniciando downloads...")
        self._download_next_in_queue()

    @Slot(str)
    def _on_mapping_error(self, err_msg: str) -> None:
        self.btn_download.setEnabled(True)
        self.btn_map_course.setEnabled(True)
        self.lbl_status.setText(f"❌ Erro ao mapear curso: {err_msg}")

    def _download_next_in_queue(self) -> None:
        if self.current_lesson_index >= len(self.lessons_queue):
            self.btn_download.setEnabled(True)
            self.btn_map_course.setEnabled(True)
            self.progress_bar.setValue(100)
            self.lbl_status.setText(f"🎉 Todos os downloads do curso foram concluídos ({len(self.lessons_queue)} aulas)!")
            return

        media_type, quality = self._get_selected_quality_params()
        lesson = self.lessons_queue[self.current_lesson_index]
        lesson_title = lesson.get('title', '') if isinstance(lesson, dict) else f"Aula {self.current_lesson_index + 1}"
        self.lbl_status.setText(f"⏳ Baixando Aula {self.current_lesson_index + 1}/{len(self.lessons_queue)}: {lesson_title}")

        user = self.txt_user.text().strip() or None
        pwd = self.txt_pass.text().strip() or None
        output_dir = self.txt_folder.text().strip()
        
        detected_course = lesson.get("course_title") or lesson.get("course") if isinstance(lesson, dict) else None
        if detected_course and detected_course != "Curso Mapeado":
            course = detected_course
            self.txt_course.setText(course)
        else:
            course = self.txt_course.text().strip() or "Curso Mapeado"

        mod_name = lesson.get("module") or lesson.get("module_name") or lesson.get("module_title") if isinstance(lesson, dict) else None
        mod_idx = lesson.get("module_index") if isinstance(lesson, dict) else None

        if not mod_name:
            mod_name = self.txt_module_name.text().strip() or "Módulo 1"
        
        if mod_idx is None:
            mod_idx = self.spin_module_idx.value()

        lesson_url = lesson.get("url") if isinstance(lesson, dict) else str(lesson)
        lesson_idx = lesson.get("index", self.current_lesson_index + 1) if isinstance(lesson, dict) else self.current_lesson_index + 1

        self.active_worker = self._create_worker(
            media_url=lesson_url,
            output_path=output_dir,
            media_type=media_type,
            quality=quality,
            username=user,
            password=pwd,
            course_name=course,
            module_name=mod_name,
            module_index=mod_idx,
            lesson_index=lesson_idx,
            lesson_name=lesson_title,
            parent=self
        )

        if not self.active_worker:
            self.lbl_status.setText(f"⚠️ Erro ao criar worker para aula {self.current_lesson_index + 1}. Pulando...")
            self.current_lesson_index += 1
            self._download_next_in_queue()
            return

        self.active_worker.progress_changed.connect(self._on_progress)
        self.active_worker.status_changed.connect(self._on_status)
        self.active_worker.download_finished.connect(self._on_batch_finished)
        self.active_worker.download_error.connect(self._on_batch_error)

        self.active_worker.start()

    def _on_progress(self, data: dict):
        percent = data.get("percent", 0)
        if hasattr(self, 'progress_bar'):
            self.progress_bar.setValue(int(percent))
            
        if hasattr(self, 'lbl_status'):
            speed = data.get("speed", "N/A")
            eta = data.get("eta", "N/A")
            self.lbl_status.setText(f"Baixando: {percent:.1f}% | Velocidade: {speed} | Tempo Restante: {eta}")

    def _on_status(self, _status_code: str, message: str):
        if hasattr(self, 'lbl_status'):
            self.lbl_status.setText(f"{message}")

    # ==========================================================
    # GERENCIAMENTO DE LINHAS DA TABELA E DOWNLOADS (ULTRA SEGURO)
    # ==========================================================

    def _add_to_table(self, title: str, filepath: str, status: str) -> None:
        """Adiciona uma linha na tabela e força a renderização visual imediata."""
        try:
            if not hasattr(self, 'table') or self.table is None:
                return

            row = self.table.rowCount()
            self.table.insertRow(row)

            num_str = f"{row + 1:02d}"
            title_str = str(title) if title else "Mídia Sem Título"
            path_str = str(filepath) if filepath else "N/A"
            status_str = str(status) if status else "Concluído"

            item_num = QTableWidgetItem(num_str)
            item_title = QTableWidgetItem(title_str)
            item_path = QTableWidgetItem(path_str)
            item_status = QTableWidgetItem(status_str)

            try:
                align_center = int(Qt.AlignmentFlag.AlignCenter) if hasattr(Qt, 'AlignmentFlag') else int(Qt.AlignCenter)
                item_num.setTextAlignment(align_center)
                item_status.setTextAlignment(align_center)
            except Exception:
                pass

            self.table.setItem(row, 0, item_num)
            self.table.setItem(row, 1, item_title)
            self.table.setItem(row, 2, item_path)
            self.table.setItem(row, 3, item_status)

            self.table.scrollToBottom()
            self.table.viewport().update()
        except Exception as e:
            print(f"❌ Erro ao adicionar item na tabela: {e}")

    @Slot(str)
    def _on_finished(self, filepath: str = "") -> None:
        """Lida com a conclusão de um download único (avulso)."""
        self.lbl_status.setText("✅ Download concluído com sucesso!")
        self.btn_download.setEnabled(True)
        self.btn_map_course.setEnabled(True)
        self.progress_bar.setValue(100)
        
        filename = os.path.basename(filepath) if filepath else "Mídia Salva"
        self._add_to_table(filename, filepath, "Concluído")

    @Slot(str)
    def _on_error(self, err_msg: str = "") -> None:
        """Lida com erro em um download único (avulso)."""
        self.lbl_status.setText(f"❌ Erro no download: {err_msg}")
        self.btn_download.setEnabled(True)
        self.btn_map_course.setEnabled(True)

    @Slot(str)
    def _on_batch_finished(self, filepath: str = "") -> None:
        """Lida com a conclusão de uma aula e puxa a próxima da fila."""
        try:
            title = ""
            if hasattr(self, 'lessons_queue') and self.lessons_queue and 0 <= self.current_lesson_index < len(self.lessons_queue):
                lesson = self.lessons_queue[self.current_lesson_index]
                if isinstance(lesson, dict):
                    title = lesson.get("title") or lesson.get("name") or ""

            if not title and filepath:
                title = os.path.basename(filepath)
            if not title:
                title = f"Aula {self.current_lesson_index + 1:02d}"

            self._add_to_table(title, filepath, "Concluído")
            print(f"✅ [Download] Arquivo salvo em: {filepath}")
        except Exception as e:
            print(f"⚠️ Erro ao atualizar tabela: {e}")
            self._add_to_table(f"Aula {self.current_lesson_index + 1:02d}", str(filepath), "Concluído")
        finally:
            self.current_lesson_index += 1
            self._download_next_in_queue()

    @Slot(str)
    def _on_batch_error(self, err_msg: str = "") -> None:
        """Lida com erro em uma aula da fila e pula para a próxima."""
        try:
            title = f"Aula {self.current_lesson_index + 1:02d}"
            if hasattr(self, 'lessons_queue') and self.lessons_queue and 0 <= self.current_lesson_index < len(self.lessons_queue):
                lesson = self.lessons_queue[self.current_lesson_index]
                if isinstance(lesson, dict):
                    title = lesson.get("title") or title

            self._add_to_table(title, "N/A", "Falha")
            print(f"❌ [Download] Erro na aula {self.current_lesson_index + 1}: {err_msg}")
        except Exception as e:
            print(f"⚠️ Erro ao registrar falha na tabela: {e}")
        finally:
            self.current_lesson_index += 1
            self._download_next_in_queue()