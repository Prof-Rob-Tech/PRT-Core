import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import PRTMainWindow
from widgets import (
    PRTButton,
    PRTCard,
    PRTSidebar,
)


def main() -> int:

    app = QApplication(sys.argv)

    window = PRTMainWindow()

    # Sidebar
    sidebar = PRTSidebar()
    
    sidebar.connect_main_window(window)

    window.add_sidebar(sidebar)

    # Card
    card = PRTCard(
        title="Downloads"
    )

    card.add_widget(
        PRTButton("Download")
    )

    #window.add_widget(card)

    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())