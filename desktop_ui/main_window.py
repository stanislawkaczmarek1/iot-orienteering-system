
from PyQt6.QtWidgets import  QMainWindow, QFrame, QVBoxLayout
from sqlalchemy.orm import Session

from backend.db.race_repository import RaceRepository

from desktop_ui.frames.race_list_frame import RaceListFrame
from desktop_ui.frames.race_creator_frame import RaceCreatorFrame
from desktop_ui.frames.header_menu_frame import HeaderMenuFrame

from desktop_ui.config import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT

class MainWindow(QMainWindow):

    MENU_ITEMS = [
        ("Race List", lambda repository: RaceListFrame(repository)),
        ("Race Creator", lambda repository: RaceCreatorFrame(repository)),
    ]

    def __init__(self, session: "Session", parent=None):
        super().__init__(parent)

        self.setWindowTitle(WINDOW_TITLE)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        race_repository = RaceRepository(session)
        
        menu_items = [
            (title, lambda repo_factory = factory: repo_factory(race_repository))
            for title, factory in MainWindow.MENU_ITEMS
        ]
        self.header_menu = HeaderMenuFrame(menu_items)
        self.header_menu.switch_to(0)

        central_widget = QFrame()
        central_layout = QVBoxLayout()
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)
        central_widget.setLayout(central_layout)

        central_layout.addWidget(self.header_menu)
        central_layout.addWidget(self.header_menu.stacked_widget) 

        self.setCentralWidget(central_widget)
