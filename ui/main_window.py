"""
===========================================================
PRT Labs - UI / Main Window
Class: PRTMainWindow

Description:
    Janela principal da aplicação PRT NEXUS integrando
    a Sidebar, navegação entre páginas e suporte dinâmico
    à bandeja do sistema (System Tray) respeitando as configurações.
===========================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QStackedWidget,
    QStyle,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

# Páginas reais do sistema
from ui.pages.courses_page import CoursesPage
from ui.pages.dashboard_page import DashboardPage
from ui.pages.downloads_page import DownloadsPage
from ui.pages.settings_page import SettingsPage


class PRTMainWindow(QMainWindow):
    """Janela principal do PRT NEXUS com suporte dinâmico ao System Tray."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PRT NEXUS")
        self.resize(1280, 800)
        self.setStyleSheet("background-color: #0E0F12;")

        # Valor padrão caso a página de configurações não especifique
        self.minimize_to_tray = True

        # Layout Principal (Horizontal: Sidebar + Conteúdo)
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        self.main_layout = QHBoxLayout(main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Área Central (Navegação de Telas)
        self.pages_stack = QStackedWidget()
        self.pages_stack.setStyleSheet("background-color: #121318;")
        self.main_layout.addWidget(self.pages_stack, stretch=1)

        self.sidebar = None
        self.page_indices: dict[str, int] = {}
        self.settings_page = None

        # 1. Instancia as telas
        self._init_pages()

        # 2. Configura a Ícone na Bandeja do Windows (System Tray)
        self._setup_system_tray()

        # 3. Abre maximizada
        self.showMaximized()

    def add_sidebar(self, sidebar) -> None:
        """Acopla a Sidebar injetada pela Application no lado esquerdo."""
        self.sidebar = sidebar
        self.main_layout.insertWidget(0, self.sidebar)

    def _init_pages(self) -> None:
        """Instancia e mapeia todas as telas reais e temporárias."""
        self.settings_page = SettingsPage()

        pages_map: dict[str, QWidget] = {
            "inicio": DashboardPage(),
            "downloads": DownloadsPage(),
            "biblioteca": CoursesPage(),
            "configuracoes": self.settings_page,
            "navegador": self._create_placeholder("🌐 Navegador Integrado", "Explore e capture mídias na web"),
            "favoritos": self._create_placeholder("⭐ Favoritos", "Conteúdos salvos para acesso rápido"),
            "historico": self._create_placeholder("🕒 Histórico", "Registro de capturas e downloads anteriores"),
            "licenca": self._create_placeholder("🛡️ Licença e Conta", "Informações do plano e autenticação"),
            "atualizacoes": self._create_placeholder("🔄 Atualizações", "Verificar novas versões do PRT NEXUS"),
            "plugins": self._create_placeholder("🧩 Gerenciador de Plugins", "Extensões e conectores instalados"),
        }

        for key, widget in pages_map.items():
            index = self.pages_stack.addWidget(widget)
            self.page_indices[key] = index

    def _create_placeholder(self, title: str, description: str) -> QWidget:
        """Cria um widget temporário para páginas em desenvolvimento."""
        page = QWidget()
        vbox = QVBoxLayout(page)
        vbox.setAlignment(Qt.AlignCenter)
        vbox.setSpacing(8)

        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("color: #FFFFFF; font-size: 22px; font-weight: bold;")

        lbl_desc = QLabel(description)
        lbl_desc.setStyleSheet("color: #71717A; font-size: 14px;")

        vbox.addWidget(lbl_title, alignment=Qt.AlignCenter)
        vbox.addWidget(lbl_desc, alignment=Qt.AlignCenter)

        return page

    def _setup_system_tray(self) -> None:
        """Cria e configura o ícone da bandeja do sistema."""
        self.tray_icon = QSystemTrayIcon(self)
        
        icon = self.style().standardIcon(QStyle.SP_ComputerIcon)
        self.tray_icon.setIcon(icon)
        self.tray_icon.setToolTip("PRT NEXUS")

        tray_menu = QMenu()
        
        action_show = tray_menu.addAction("Abrir PRT NEXUS")
        action_show.triggered.connect(self.restore_from_tray)

        tray_menu.addSeparator()

        action_quit = tray_menu.addAction("Sair do PRT NEXUS")
        action_quit.triggered.connect(self.quit_application)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self._on_tray_icon_activated)
        self.tray_icon.show()

    def _on_tray_icon_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        """Trata cliques no ícone da bandeja."""
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            if self.isVisible():
                self.hide()
            else:
                self.restore_from_tray()

    def restore_from_tray(self) -> None:
        """Restaura a janela visível na tela."""
        self.show()
        self.showMaximized()
        self.activateWindow()

    def quit_application(self) -> None:
        """Encerra a aplicação definitivamente."""
        self.tray_icon.hide()
        QApplication.quit()

    def _is_minimize_to_tray_enabled(self) -> bool:
        """Verifica dinamicamente na página de configurações se a opção está marcada."""
        if self.settings_page:
            # Tenta encontrar o checkbox da tela de configurações por atributos conhecidos
            for attr in ("chk_tray", "chk_minimize_to_tray", "tray_checkbox"):
                if hasattr(self.settings_page, attr):
                    return getattr(self.settings_page, attr).isChecked()
            
            # Tenta via método de leitura se existir
            if hasattr(self.settings_page, "get_minimize_to_tray"):
                return self.settings_page.get_minimize_to_tray()

        return self.minimize_to_tray

    def _on_page_changed(self, page_key: str) -> None:
        """Muda a página visível com base na seleção da Sidebar."""
        print(f"[PRT NEXUS] Navegando para: {page_key}")
        if page_key in self.page_indices:
            self.pages_stack.setCurrentIndex(self.page_indices[page_key])

    def closeEvent(self, event: QCloseEvent) -> None:
        """Intercepta o clique no botão fechar (X)."""
        should_minimize = self._is_minimize_to_tray_enabled()

        if should_minimize:
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "PRT NEXUS",
                "O aplicativo continua rodando em segundo plano.",
                QSystemTrayIcon.Information,
                2000,
            )
        else:
            self.tray_icon.hide()
            event.accept()
            QApplication.quit()