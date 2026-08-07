"""
===========================================================
PRT Labs - UI / Dialogs
Class: CourseMapperDialog

Description:
    Modal de Mapeamento Automático de Módulos e Aulas.
    Exibe a árvore do curso (Módulos e Aulas) com checkboxes,
    resumo de seleção em tempo real e envio em lote para a fila.
===========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
)


class CourseMapperDialog(QDialog):
    """Modal interativo para mapear, selecionar e enviar módulos e aulas para a fila."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("PRT NEXUS - Mapeador de Módulos e Aulas")
        self.resize(850, 600)
        self.setMinimumSize(700, 500)
        self.setStyleSheet(
            """
            QDialog {
                background-color: #121318;
                color: #FFFFFF;
            }
        """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        # 1. Instancia a Árvore de Módulos PRIMEIRO para evitar o AttributeError
        self.tree = self._create_tree_widget()

        # 2. Cabeçalho
        layout.addWidget(self._create_header())

        # 3. Barra de Ações Rápidas (Busca e Selecionar Todos)
        layout.addLayout(self._create_toolbar())

        # 4. Adiciona a Árvore ao Layout
        layout.addWidget(self.tree, stretch=1)

        # 5. Carrega os dados do curso de exemplo
        self._load_demo_course_tree()

        # 6. Rodapé (Resumo de Seleção e Botões)
        layout.addLayout(self._create_footer())

        # Conecta eventos de alteração de seleção após todos os componentes existirem
        self.tree.itemChanged.connect(self._on_item_changed)
        self._update_selection_summary()

    def _create_header(self) -> QFrame:
        """Cria o cabeçalho estilizado do modal."""
        header = QFrame()
        header.setStyleSheet(
            """
            QFrame {
                background-color: #18181B;
                border: 1px solid #27272A;
                border-radius: 8px;
            }
        """
        )
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(16, 12, 16, 12)

        v_text = QVBoxLayout()
        v_text.setSpacing(4)
        lbl_title = QLabel("🍒 Mapeamento Automático de Módulos e Aulas")
        lbl_title.setStyleSheet("color: #FFFFFF; font-size: 18px; font-weight: bold;")

        lbl_subtitle = QLabel("Curso Detectado: Formação Full Stack Pro (Kiwify / Nutror)")
        lbl_subtitle.setStyleSheet("color: #A1A1AA; font-size: 13px;")

        v_text.addWidget(lbl_title)
        v_text.addWidget(lbl_subtitle)

        h_layout.addLayout(v_text)
        h_layout.addStretch()

        # Badge de estatísticas do curso
        lbl_badge = QLabel(" 4 Módulos | 12 Aulas ")
        lbl_badge.setStyleSheet(
            """
            QLabel {
                background-color: #27272A;
                color: #6366F1;
                font-weight: bold;
                font-size: 12px;
                padding: 6px 12px;
                border-radius: 12px;
                border: 1px solid #6366F1;
            }
        """
        )
        h_layout.addWidget(lbl_badge)

        return header

    def _create_toolbar(self) -> QHBoxLayout:
        """Cria a barra de ferramentas superior com filtro e seleção rápida."""
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        self.chk_select_all = QCheckBox("Selecionar Tudo")
        self.chk_select_all.setChecked(True)
        self.chk_select_all.setStyleSheet("color: #FFFFFF; font-weight: bold;")
        self.chk_select_all.stateChanged.connect(self._toggle_select_all)

        btn_expand = QPushButton("Expandir Todos")
        btn_collapse = QPushButton("Recolher Todos")

        for btn in (btn_expand, btn_collapse):
            btn.setStyleSheet(
                """
                QPushButton {
                    background-color: #18181B;
                    color: #A1A1AA;
                    border: 1px solid #27272A;
                    border-radius: 6px;
                    padding: 6px 12px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #27272A;
                    color: #FFFFFF;
                }
            """
            )

        btn_expand.clicked.connect(self.tree.expandAll)
        btn_collapse.clicked.connect(self.tree.collapseAll)

        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("🔍 Pesquisar aula por nome...")
        self.txt_search.setStyleSheet(
            """
            QLineEdit {
                background-color: #18181B;
                color: #FFFFFF;
                border: 1px solid #27272A;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 1px solid #6366F1;
            }
        """
        )
        self.txt_search.textChanged.connect(self._filter_tree)

        toolbar.addWidget(self.chk_select_all)
        toolbar.addWidget(btn_expand)
        toolbar.addWidget(btn_collapse)
        toolbar.addWidget(self.txt_search, stretch=1)

        return toolbar

    def _create_tree_widget(self) -> QTreeWidget:
        """Cria o componente visual de árvore estilizado."""
        tree = QTreeWidget()
        tree.setHeaderLabels(["Módulo / Nome da Aula", "Player / Formato", "Duração"])
        tree.header().setSectionResizeMode(0, QHeaderView.Stretch)
        tree.header().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        tree.header().setSectionResizeMode(2, QHeaderView.ResizeToContents)

        tree.setStyleSheet(
            """
            QTreeWidget {
                background-color: #0E0F12;
                color: #FFFFFF;
                border: 1px solid #27272A;
                border-radius: 8px;
                outline: none;
            }
            QTreeWidget::item {
                padding: 6px;
                border-bottom: 1px solid #18181B;
            }
            QTreeWidget::item:hover {
                background-color: #18181B;
            }
            QTreeWidget::item:selected {
                background-color: #27272A;
                color: #FFFFFF;
            }
            QHeaderView::section {
                background-color: #18181B;
                color: #A1A1AA;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """
        )
        return tree

    def _load_demo_course_tree(self) -> None:
        """Preenche a árvore com dados de exemplo (Módulos e Aulas)."""
        modules = [
            {
                "title": "Módulo 01 - Boas-Vindas e Primeiros Passos",
                "lessons": [
                    ("Aula 01 - Apresentação da Plataforma", "HLS / Vimeo (1080p)", "12 min"),
                    ("Aula 02 - Como Usar o Suporte", "HLS / Vimeo (1080p)", "08 min"),
                    ("Aula 03 - Download de Materiais Auxiliares", "Panda Video (720p)", "15 min"),
                ],
            },
            {
                "title": "Módulo 02 - Estrutura de Arquitetura",
                "lessons": [
                    ("Aula 01 - Visão Geral dos Componentes", "M3U8 Stream (1080p)", "25 min"),
                    ("Aula 02 - Configuração da Janela Principal", "M3U8 Stream (1080p)", "32 min"),
                    ("Aula 03 - Integração de UI e Layout", "Panda Video (1080p)", "20 min"),
                    ("Aula 04 - Boas Práticas e Organização", "HLS / Vimeo (1080p)", "18 min"),
                ],
            },
            {
                "title": "Módulo 03 - Interceptação e Automação",
                "lessons": [
                    ("Aula 01 - Mapeamento de Requisições HTTP", "HLS / Vimeo (1080p)", "40 min"),
                    ("Aula 02 - Extração de Links M3U8 e MP4", "M3U8 Stream (1080p)", "28 min"),
                    ("Aula 03 - Construção da Fila de Downloads", "Panda Video (1080p)", "35 min"),
                ],
            },
            {
                "title": "Módulo 04 - Segurança e Licenciamento",
                "lessons": [
                    ("Aula 01 - Validação de Chaves de Licença", "M3U8 Stream (1080p)", "22 min"),
                    ("Aula 02 - Bloqueio e Liberação de Módulos", "HLS / Vimeo (1080p)", "19 min"),
                ],
            },
        ]

        self.tree.blockSignals(True)
        for mod in modules:
            mod_item = QTreeWidgetItem(self.tree)
            mod_item.setText(0, f"📁 {mod['title']}")
            mod_item.setFlags(mod_item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsAutoTristate)
            mod_item.setCheckState(0, Qt.Checked)

            for title, player, dur in mod["lessons"]:
                child = QTreeWidgetItem(mod_item)
                child.setText(0, f"▶ {title}")
                child.setText(1, player)
                child.setText(2, dur)
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setCheckState(0, Qt.Checked)

            mod_item.setExpanded(True)

        self.tree.blockSignals(False)

    def _toggle_select_all(self, state: int) -> None:
        """Seleciona ou desmarca todos os itens da árvore."""
        check_state = Qt.Checked if state == Qt.Checked.value else Qt.Unchecked
        self.tree.blockSignals(True)

        root = self.tree.invisibleRootItem()
        for i in range(root.childCount()):
            mod_item = root.child(i)
            mod_item.setCheckState(0, check_state)
            for j in range(mod_item.childCount()):
                mod_item.child(j).setCheckState(0, check_state)

        self.tree.blockSignals(False)
        self._update_selection_summary()

    def _on_item_changed(self, item: QTreeWidgetItem, column: int) -> None:
        """Atualiza a contagem sempre que o estado de um checkbox muda."""
        self._update_selection_summary()

    def _update_selection_summary(self) -> None:
        """Calcula em tempo real o total de aulas selecionadas."""
        selected_count = 0
        total_count = 0

        root = self.tree.invisibleRootItem()
        for i in range(root.childCount()):
            mod_item = root.child(i)
            for j in range(mod_item.childCount()):
                total_count += 1
                if mod_item.child(j).checkState(0) == Qt.Checked:
                    selected_count += 1

        self.lbl_summary.setText(f"Aulas Selecionadas: {selected_count} de {total_count}")
        self.btn_add_to_queue.setText(f"⚡ Adicionar {selected_count} Aulas à Fila")
        self.btn_add_to_queue.setEnabled(selected_count > 0)

    def _filter_tree(self, text: str) -> None:
        """Filtra as aulas e módulos na árvore em tempo real."""
        text = text.lower()
        root = self.tree.invisibleRootItem()
        for i in range(root.childCount()):
            mod_item = root.child(i)
            mod_match = text in mod_item.text(0).lower()
            any_child_match = False

            for j in range(mod_item.childCount()):
                child = mod_item.child(j)
                child_match = text in child.text(0).lower() or text in child.text(1).lower()
                child.setHidden(not child_match and not mod_match)
                if child_match:
                    any_child_match = True

            mod_item.setHidden(not mod_match and not any_child_match)

    def _create_footer(self) -> QHBoxLayout:
        """Cria o rodapé do modal com botões de confirmação e cancelamento."""
        footer = QHBoxLayout()
        footer.setSpacing(12)

        self.lbl_summary = QLabel("Aulas Selecionadas: 0 de 0")
        self.lbl_summary.setStyleSheet("color: #A1A1AA; font-weight: bold; font-size: 13px;")

        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setStyleSheet(
            """
            QPushButton {
                background-color: #27272A;
                color: #FFFFFF;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3F3F46;
            }
        """
        )
        btn_cancel.clicked.connect(self.reject)

        self.btn_add_to_queue = QPushButton("⚡ Adicionar Aulas à Fila")
        self.btn_add_to_queue.setStyleSheet(
            """
            QPushButton {
                background-color: #6366F1;
                color: #FFFFFF;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #4F46E5;
            }
            QPushButton:disabled {
                background-color: #27272A;
                color: #71717A;
            }
        """
        )
        self.btn_add_to_queue.clicked.connect(self.accept)

        footer.addWidget(self.lbl_summary)
        footer.addStretch()
        footer.addWidget(btn_cancel)
        footer.addWidget(self.btn_add_to_queue)

        return footer