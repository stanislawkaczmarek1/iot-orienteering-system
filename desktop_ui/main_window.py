from PyQt6.QtWidgets import QMainWindow, QFrame, QVBoxLayout
from sqlalchemy.orm import Session

from desktop_ui.frames.dashboard_frame import DashboardFrame
from desktop_ui.frames.race_list_frame import RaceListFrame
from desktop_ui.frames.race_creator_frame import RaceCreatorFrame
from desktop_ui.frames.header_menu_frame import HeaderMenuFrame

from desktop_ui.config import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT
from desktop_ui.services.race_service import RaceService


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.race_service = RaceService()
        self.menu_items = [
            ("Dashboard", lambda: DashboardFrame(self.race_service)),
            ("Race List", lambda: RaceListFrame(self.race_service)),
            ("Race Creator", lambda: RaceCreatorFrame(self.race_service)),
        ]

        self.setWindowTitle(WINDOW_TITLE)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.header_menu = HeaderMenuFrame(self.menu_items)
        self.header_menu.switch_to(0)

        central_widget = QFrame()
        central_layout = QVBoxLayout()
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)
        central_widget.setLayout(central_layout)

        central_layout.addWidget(self.header_menu)
        central_layout.addWidget(self.header_menu.stacked_widget)

        self.setCentralWidget(central_widget)
