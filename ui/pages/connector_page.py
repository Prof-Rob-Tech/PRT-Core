"""
===========================================================
PRT Labs - UI / Pages
Class: ConnectorPage
Description: Template genérico e adaptável para conectores com suporte a
             Login/Senha, criação de estrutura de pastas e downloads via PRTDownloadWorker.
===========================================================
"""

import os
from PySide6.QtCore import Qt, QThread, Signal
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
        from download_worker import PRTDownloadWorker, UniversoCourseMapper # type: ignore
    except ImportError:
        PRTDownloadWorker = None
        UniversoCourseMapper = None


class CourseMapThread(QThread):
    """Thread em segundo plano para não travar a interface durante o mapeamento com Playwright."""
    finished_signal = Signal(list)
    error_signal = Signal(str)

    def __init__(self, course_url, username, password, parent=None):
        super().__init__(parent)
        self.course_url = course_url
        self.username = username
        self.password = password

    def run(self):
        try:
            if not UniversoCourseMapper:
                self.error_signal.emit("Módulo UniversoCourseMapper não encontrado.")
                return

            mapper = UniversoCourseMapper(username=self.username, password=self.password)
            lessons = mapper.map_course(self.course_url)
            self.finished_signal.emit(lessons)
        except Exception as e:
            self.error_signal.emit(str(e))


class ConnectorPage(QWidget):
    """Página de Conector Genérica adaptável aos temas do PRT Nexus."""

    def __init__(self, platform_key: str = "conector", connector_name: str = "Conector", parent=None) -> None:
        super().__init__(parent)
        self.platform_key = platform_key.lower()
        self.connector_name = connector_name.capitalize()
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

        # Linha URL + Formato + Botões
        input_layout = QHBoxLayout()
        self.txt_url = QLineEdit()
        self.txt_url.setPlaceholderText(f"Cole o link da aula ou curso do {self.connector_name} aqui (ex: https://...)")

        self.combo_format = QComboBox()
        self.combo_format.addItems(["📹 Vídeo (MP4)", "🎵 Apenas Áudio (MP3)"])

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

        # BLOCO DE AUTENTICAÇÃO / LOGIN DA PLATAFORMA
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

        # Estruturação Hierárquica de Curso
        struct_group = QVBoxLayout()
        struct_lbl = QLabel("📁 Organização de Pastas do Curso (Opcional):")
        struct_lbl.setStyleSheet("color: #A1A1AA; font-size: 12px; font-weight: bold; margin-top: 4px;")
        struct_group.addWidget(struct_lbl)

        # Nome do Curso
        self.txt_course = QLineEdit()
        self.txt_course.setPlaceholderText("Nome do Curso (ex: Nivel 2 Curso EAD Consertos de placa iPhone)")
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

        # 3. Tabela de Mídias Concluídas
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

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Título / Nome do Arquivo", "Caminho Salvo", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setFixedHeight(180)

        t_layout.addWidget(self.table)
        layout.addWidget(card_table)

        layout.addStretch()

    def _select_folder(self) -> None:
        """Abre a caixa de diálogo para escolher a pasta de saída."""
        chosen = QFileDialog.getExistingDirectory(self, "Selecione a Pasta de Destino", self.txt_folder.text())
        if chosen:
            self.txt_folder.setText(chosen)

    def _start_download(self) -> None:
        """Inicia o download enviando a URL, credenciais e parâmetros de pasta."""
        url = self.txt_url.text().strip()
        if not url:
            self.lbl_status.setText("⚠️ Digite ou cole uma URL válida antes de baixar.")
            return

        if not PRTDownloadWorker:
            self.lbl_status.setText("❌ Erro: O módulo 'download_worker' não foi encontrado.")
            return

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
        self.lbl_status.setText("🚀 Autenticando e iniciando o worker de download...")

        self.active_worker = PRTDownloadWorker(
            media_url=url,
            output_path=output_dir,
            username=user,
            password=pwd,
            course_name=course,
            module_index=mod_idx,
            module_name=mod_name,
            lesson_index=les_idx,
            lesson_name=les_name,
            parent=self
        )

        self.active_worker.progress_changed.connect(self._on_progress)
        self.active_worker.status_changed.connect(self._on_status)
        self.active_worker.download_finished.connect(self._on_finished)
        self.active_worker.download_error.connect(self._on_error)

        self.active_worker.start()

    def _start_course_mapping(self) -> None:
        """Dispara a thread de mapeamento de todas as aulas do curso via Playwright."""
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

    def _on_mapping_finished(self, lessons: list) -> None:
        """Recebe a lista de aulas mapeadas e inicia o download da primeira."""
        self.btn_download.setEnabled(True)
        self.btn_map_course.setEnabled(True)

        if not lessons:
            self.lbl_status.setText("⚠️ Nenhuma aula foi encontrada na página digitada.")
            return

        self.lessons_queue = lessons
        self.current_lesson_index = 0
        self.lbl_status.setText(f"✅ Mapeamento concluído! Total de {len(lessons)} aulas encontradas. Iniciando downloads...")
        self._download_next_in_queue()

    def _on_mapping_error(self, err_msg: str) -> None:
        self.btn_download.setEnabled(True)
        self.btn_map_course.setEnabled(True)
        self.lbl_status.setText(f"❌ Erro ao mapear curso: {err_msg}")

    def _download_next_in_queue(self) -> None:
        """Baixa em lote uma aula por vez da fila mapeada."""
        if self.current_lesson_index >= len(self.lessons_queue):
            self.lbl_status.setText(f"🎉 Todos os downloads do curso foram concluídos ({len(self.lessons_queue)} aulas)!")
            return

        lesson = self.lessons_queue[self.current_lesson_index]
        self.lbl_status.setText(f"⏳ Baixando Aula {self.current_lesson_index + 1}/{len(self.lessons_queue)}: {lesson.get('title', '')}")

        user = self.txt_user.text().strip() or None
        pwd = self.txt_pass.text().strip() or None
        output_dir = self.txt_folder.text().strip()
        course = self.txt_course.text().strip() or "Curso Mapeado"

        self.active_worker = PRTDownloadWorker(
            media_url=lesson.get("url"),
            output_path=output_dir,
            username=user,
            password=pwd,
            course_name=course,
            module_name=lesson.get("module", "Módulo 1"),
            lesson_index=lesson.get("index", self.current_lesson_index + 1),
            lesson_name=lesson.get("title"),
            parent=self
        )

        self.active_worker.progress_changed.connect(self._on_progress)
        self.active_worker.status_changed.connect(self._on_status)
        self.active_worker.download_finished.connect(self._on_batch_finished)
        self.active_worker.download_error.connect(self._on_batch_error)

        self.active_worker.start()

    def _on_batch_finished(self, file_path: str) -> None:
        self._on_finished(file_path)
        self.current_lesson_index += 1
        self._download_next_in_queue()

    def _on_batch_error(self, err_msg: str) -> None:
        self.lbl_status.setText(f"⚠️ Erro na aula {self.current_lesson_index + 1}: {err_msg}. Pula para a próxima...")
        self.current_lesson_index += 1
        self._download_next_in_queue()

    def _on_progress(self, data: dict) -> None:
        percent = int(data.get("percent", 0))
        speed = data.get("speed", "N/A")
        eta = data.get("eta", "N/A")
        
        self.progress_bar.setValue(percent)
        self.lbl_status.setText(f"⬇️ Baixando: {percent}% | Velocidade: {speed} | Restante: {eta}")

    def _on_status(self, code: str, msg: str) -> None:
        if code == "DOWNLOADING":
            self.lbl_status.setText(f"⏳ {msg}")
        elif code == "COMPLETED":
            self.lbl_status.setText(f"✅ {msg}")

    def _on_finished(self, file_path: str) -> None:
        self.btn_download.setEnabled(True)
        self.btn_map_course.setEnabled(True)
        self.progress_bar.setValue(100)

        row = self.table.rowCount()
        self.table.insertRow(row)
        
        filename = os.path.basename(file_path)
        self.table.setItem(row, 0, QTableWidgetItem(filename))
        self.table.setItem(row, 1, QTableWidgetItem(file_path))
        self.table.setItem(row, 2, QTableWidgetItem("Concluído"))

    def _on_error(self, err_msg: str) -> None:
        self.btn_download.setEnabled(True)
        self.btn_map_course.setEnabled(True)
        self.lbl_status.setText(f"❌ Erro no download: {err_msg}")