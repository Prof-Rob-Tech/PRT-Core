"""
===========================================================
PRT Labs - UI Pages / Connector Page
Class: ConnectorPage
Description: Interface gráfica genérica para conectores do PRT Nexus.
             Suporta dinamicamente múltiplas plataformas (Universo Técnico,
             YouTube, Hotmart, Kiwify, etc.), gerenciando mapeamento
             e download em fila com segurança de threads.
===========================================================
"""

import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QProgressBar, QTableWidget,
    QTableWidgetItem, QHeaderView, QFileDialog, QFrame,
    QAbstractItemView
)
from PySide6.QtCore import Qt, QThread, Signal, Slot, QTimer
from PySide6.QtGui import QFont, QIcon, QColor

# Tentativa de importação dos Workers e Mappers
try:
    from core.download.download_worker import PRTDownloadWorker, UniversoCourseMapper
except ImportError:
    PRTDownloadWorker = None
    UniversoCourseMapper = None


class CourseMapperWorker(QThread):
    """Worker em background para mapear a estrutura de cursos sem congelar a UI."""
    mapping_finished = Signal(dict)
    mapping_error = Signal(str)

    def __init__(self, url: str, username: str = None, password: str = None, parent=None):
        super().__init__(parent)
        self.url = url
        self.username = username
        self.password = password

    def run(self):
        try:
            if UniversoCourseMapper is None:
                raise ImportError("Módulo UniversoCourseMapper não foi encontrado em core.download.download_worker")
            
            mapper = UniversoCourseMapper(username=self.username, password=self.password)
            result = mapper.map_course(self.url)
            self.mapping_finished.emit(result)
        except Exception as e:
            self.mapping_error.emit(str(e))


class ConnectorPage(QWidget):
    """Página adaptável para conectores de plataforma."""

    def __init__(
        self, 
        platform_key: str = "universo", 
        connector_name: str = "Universo Técnico", 
        parent=None, 
        **kwargs
    ):
        super().__init__(parent)
        
        self.platform_key = platform_key
        self.connector_name = connector_name

        # Variáveis de Controle da Fila de Downloads
        self.lessons_queue = []
        self.current_lesson_index = 0
        self.active_worker = None
        self.mapper_thread = None

        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # -------------------------------------------------------------
        # CABEÇALHO DA PÁGINA
        # -------------------------------------------------------------
        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)

        lbl_title = QLabel(f"🔗 Conector {self.connector_name}")
        lbl_title.setFont(QFont("Segoe UI", 16, QFont.Bold))

        lbl_subtitle = QLabel(f"Capture, extraia e gerencie conteúdos diretamente do {self.connector_name}.")
        lbl_subtitle.setFont(QFont("Segoe UI", 10))

        header_layout.addWidget(lbl_title)
        header_layout.addWidget(lbl_subtitle)
        main_layout.addLayout(header_layout)

        # -------------------------------------------------------------
        # PAINEL PRINCIPAL DE FORMULÁRIO / CONFIGURAÇÃO
        # -------------------------------------------------------------
        card_box = QFrame()
        card_box.setObjectName("cardFrame")

        card_layout = QVBoxLayout(card_box)
        card_layout.setSpacing(14)
        card_layout.setContentsMargins(16, 16, 16, 16)

        # Section Label 1
        lbl_sec1 = QLabel(f"🔗 Capturar Mídia via URL - {self.connector_name}")
        lbl_sec1.setFont(QFont("Segoe UI", 11, QFont.Bold))
        card_layout.addWidget(lbl_sec1)

        # LINHA 1: URL + Formato + Botões
        row1 = QHBoxLayout()
        row1.setSpacing(10)

        self.txt_url = QLineEdit()
        self.txt_url.setPlaceholderText("Insira a URL do vídeo ou curso...")
        
        self.cmb_quality = QComboBox()
        self.cmb_quality.addItems([
            "Vídeo - Max Qualidade (MP4)",
            "Vídeo - 1080p (MP4)",
            "Vídeo - 720p (MP4)",
            "Áudio - Apenas Som (MP3)"
        ])

        self.btn_download_single = QPushButton("⬇️ Baixar Mídia")

        self.btn_map_and_download = QPushButton("📚 Mapear e Baixar Curso")
        self.btn_map_and_download.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #059669;
            }
            QPushButton:disabled {
                background-color: #064e3b;
                color: #6ee7b7;
            }
        """)
        self.btn_map_and_download.clicked.connect(self._start_mapping)

        row1.addWidget(self.txt_url, 4)
        row1.addWidget(self.cmb_quality, 2)
        row1.addWidget(self.btn_download_single, 1)
        row1.addWidget(self.btn_map_and_download, 2)
        card_layout.addLayout(row1)

        # LINHA 2: Autenticação
        lbl_sec2 = QLabel(f"🔒 Autenticação / Conta {self.connector_name} (Necessário para áreas pagas):")
        card_layout.addWidget(lbl_sec2)

        row2 = QHBoxLayout()
        row2.setSpacing(10)

        self.txt_username = QLineEdit()
        self.txt_username.setPlaceholderText("Seu email de acesso")

        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.Password)
        self.txt_password.setPlaceholderText("Sua senha de acesso")

        row2.addWidget(self.txt_username, 1)
        row2.addWidget(self.txt_password, 1)
        card_layout.addLayout(row2)

        # LINHA 3: Organização de Pastas do Curso
        lbl_sec3 = QLabel("📁 Organização de Pastas do Curso (Detectado automaticamente ou personalize):")
        card_layout.addWidget(lbl_sec3)

        self.txt_course_name = QLineEdit()
        self.txt_course_name.setPlaceholderText("Nome do Curso")
        card_layout.addWidget(self.txt_course_name)

        row3 = QHBoxLayout()
        row3.setSpacing(10)

        self.cmb_module = QComboBox()
        self.cmb_module.addItems(["Mod 1", "Mod 2", "Mod 3", "Mod 4", "Mod 5"])

        self.txt_module_name = QLineEdit()
        self.txt_module_name.setPlaceholderText("Nome do Módulo")

        self.cmb_lesson = QComboBox()
        self.cmb_lesson.addItems(["Aula 1", "Aula 2", "Aula 3", "Aula 4", "Aula 5"])

        self.txt_lesson_name = QLineEdit()
        self.txt_lesson_name.setPlaceholderText("Nome da Aula")

        row3.addWidget(self.cmb_module, 1)
        row3.addWidget(self.txt_module_name, 2)
        row3.addWidget(self.cmb_lesson, 1)
        row3.addWidget(self.txt_lesson_name, 2)
        card_layout.addLayout(row3)

        # LINHA 4: Diretório de Destino
        row4 = QHBoxLayout()
        row4.setSpacing(10)

        default_download_path = os.path.join(os.path.expanduser("~"), "Downloads", "PRT_Nexus")
        self.txt_output_dir = QLineEdit(default_download_path)

        self.btn_browse = QPushButton("📁 Alterar Pasta")
        self.btn_browse.clicked.connect(self._browse_folder)

        row4.addWidget(self.txt_output_dir, 4)
        row4.addWidget(self.btn_browse, 1)
        card_layout.addLayout(row4)

        # LINHA 5: Barra de Progresso e Status Label
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)

        self.lbl_status = QLabel("⏳ Pronto para iniciar.")

        card_layout.addWidget(self.progress_bar)
        card_layout.addWidget(self.lbl_status)

        main_layout.addWidget(card_box)

        # -------------------------------------------------------------
        # TABELA DE MÍDIAS CONCLUÍDAS
        # -------------------------------------------------------------
        table_box = QFrame()
        table_box.setObjectName("cardFrame")

        table_layout = QVBoxLayout(table_box)
        table_layout.setContentsMargins(16, 16, 16, 16)

        lbl_sec_table = QLabel(f"📦 Mídias Concluídas do {self.connector_name}")
        lbl_sec_table.setFont(QFont("Segoe UI", 11, QFont.Bold))
        table_layout.addWidget(lbl_sec_table)

        self.table_completed = QTableWidget(0, 3)
        self.table_completed.setHorizontalHeaderLabels(["Título / Nome do Arquivo", "Caminho Salvo", "Status"])
        self.table_completed.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_completed.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        header = self.table_completed.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

        table_layout.addWidget(self.table_completed)
        main_layout.addWidget(table_box, 1)

    # -----------------------------------------------------------------
    # MÉTODOS DE AÇÃO E NAVEGAÇÃO
    # -----------------------------------------------------------------

    def _browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Selecionar Pasta de Destino", self.txt_output_dir.text())
        if folder:
            self.txt_output_dir.setText(folder)

    def _start_mapping(self):
        url = self.txt_url.text().strip()
        if not url:
            self.lbl_status.setText("⚠️ Por favor, insira a URL do curso primeiro!")
            return

        self.btn_map_and_download.setEnabled(False)
        self.lbl_status.setText("⌛ Mapeando catálogo do curso e estrutura de aulas...")
        self.progress_bar.setValue(0)

        # Instancia worker de mapeamento em background
        self.mapper_thread = CourseMapperWorker(
            url=url,
            username=self.txt_username.text().strip(),
            password=self.txt_password.text().strip()
        )
        self.mapper_thread.mapping_finished.connect(self._on_mapping_finished)
        self.mapper_thread.mapping_error.connect(self._on_mapping_error)
        self.mapper_thread.start()

    @Slot(dict)
    def _on_mapping_finished(self, data: dict):
        course_title = data.get("course_title", "Curso Mapeado")
        self.lessons_queue = data.get("lessons", [])

        if course_title and course_title != "Curso Mapeado":
            self.txt_course_name.setText(course_title)

        if not self.lessons_queue:
            self.lbl_status.setText("⚠️ Nenhum link de aula encontrado na página do curso informada.")
            self.btn_map_and_download.setEnabled(True)
            return

        self.lbl_status.setText(f"✅ Mapeamento concluído! {len(self.lessons_queue)} aulas encontradas. Iniciando downloads...")
        self.current_lesson_index = 0
        
        # Inicia a fila de downloads
        self._download_next_in_queue()

    @Slot(str)
    def _on_mapping_error(self, err_msg: str):
        self.lbl_status.setText(f"❌ Erro ao mapear curso: {err_msg}")
        self.btn_map_and_download.setEnabled(True)

    # -----------------------------------------------------------------
    # GERENCIAMENTO SEGURO DE THREADS DE DOWNLOAD
    # -----------------------------------------------------------------

    def _download_next_in_queue(self):
        """Inicia o download da próxima aula da fila com gerenciamento seguro de threads."""
        if not hasattr(self, 'lessons_queue') or self.current_lesson_index >= len(self.lessons_queue):
            self.lbl_status.setText("🎉 Todos os downloads concluídos!")
            self.progress_bar.setValue(100)
            self.btn_map_and_download.setEnabled(True)
            return

        lesson = self.lessons_queue[self.current_lesson_index]
        self.lbl_status.setText(
            f"⌛ Processando aula {self.current_lesson_index + 1}/{len(self.lessons_queue)}: {lesson.get('title', '')}..."
        )

        # Encerramento seguro sem disparar exceções no C++ / Shiboken
        if getattr(self, 'active_worker', None) is not None:
            try:
                if self.active_worker.isRunning():
                    self.active_worker.quit()
                    self.active_worker.wait(1000)
            except RuntimeError:
                # Objeto C++ já desalocado pelo Qt
                pass
            self.active_worker = None

        if PRTDownloadWorker is None:
            self.lbl_status.setText("❌ Erro: PRTDownloadWorker não importado.")
            self.btn_map_and_download.setEnabled(True)
            return

        # Cria a nova thread
        self.active_worker = PRTDownloadWorker(
            media_url=lesson.get('url', ''),
            output_path=self.txt_output_dir.text().strip(),
            username=self.txt_username.text().strip(),
            password=self.txt_password.text().strip(),
            course_name=self.txt_course_name.text().strip() or lesson.get('course_title', 'Curso Mapeado'),
            module_name=lesson.get('module', 'Módulo 1'),
            lesson_index=lesson.get('index', self.current_lesson_index + 1),
            lesson_name=lesson.get('title', 'Aula'),
            parent=self  # Define o parent no Qt para retenção de memória correta
        )

        self.active_worker.progress_changed.connect(self._update_progress_bar)
        self.active_worker.status_changed.connect(self._update_status_label)
        self.active_worker.download_finished.connect(self._on_batch_finished)
        self.active_worker.download_error.connect(self._on_batch_error)

        self.active_worker.start()
        
    @Slot(dict)
    def _update_progress_bar(self, progress_data: dict):
        percent = progress_data.get("percent", 0)
        speed = progress_data.get("speed", "N/A")
        eta = progress_data.get("eta", "N/A")
        
        self.progress_bar.setValue(int(percent))
        if percent < 100:
            self.lbl_status.setText(f"🚀 Baixando: {percent:.1f}% | Velocidade: {speed} | ETA: {eta}")

    @Slot(str, str)
    def _update_status_label(self, status: str, text: str):
        self.lbl_status.setText(text)

    @Slot(str)
    def _on_batch_finished(self, file_path: str) -> None:
        """Handler disparado quando o download da aula atual finaliza com sucesso."""
        self._add_completed_to_table(file_path)
        self.current_lesson_index += 1
        
        # Delay de 300ms garante desalocação completa da thread no Qt antes do novo ciclo
        QTimer.singleShot(300, self._download_next_in_queue)

    @Slot(str)
    def _on_batch_error(self, err_msg: str) -> None:
        """Handler disparado quando ocorre um erro ou a aula é teórica/sem vídeo."""
        print(f"[{self.connector_name}] {err_msg}")
        self.lbl_status.setText(f"⚠️ {err_msg} -> Pulando para a próxima...")
        
        self.current_lesson_index += 1
        
        # Avança para a próxima aula sem quebrar o loop do curso
        QTimer.singleShot(300, self._download_next_in_queue)

    def _add_completed_to_table(self, file_path: str):
        row_idx = self.table_completed.rowCount()
        self.table_completed.insertRow(row_idx)

        file_name = os.path.basename(file_path) if file_path else "Mídia Desconhecida"
        
        item_title = QTableWidgetItem(file_name)
        item_path = QTableWidgetItem(file_path or "N/A")
        item_status = QTableWidgetItem("Concluído ✅")
        item_status.setForeground(QColor("#10b981"))

        self.table_completed.setItem(row_idx, 0, item_title)
        self.table_completed.setItem(row_idx, 1, item_path)
        self.table_completed.setItem(row_idx, 2, item_status)