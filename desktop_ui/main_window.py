
from PyQt6.QtWidgets import  QMainWindow, QFrame, QVBoxLayout
from sqlalchemy.orm import Session

from backend.db.race_repository import RaceRepository
from backend.db.models import Race

from desktop_ui.frames.race_list_frame import RaceListFrame
from desktop_ui.frames.race_creator_frame import RaceCreatorFrame
from desktop_ui.frames.race_detail_frame import RaceDetailFrame
from desktop_ui.frames.header_menu_frame import HeaderMenuPackedFrame

from desktop_ui.config import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT

class MainWindow(QMainWindow):
    MENU_ITEMS = [
        ("Race List", "race_list"),
        ("Race Creator", "race_creator"),
    ]

    def __init__(self, session: "Session", parent=None):
        super().__init__(parent)

        self.setWindowTitle(WINDOW_TITLE)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.race_repository = RaceRepository(session)

        self.container = HeaderMenuPackedFrame(self.MENU_ITEMS)
        self.setCentralWidget(self.container)

        self.race_list_frame = RaceListFrame(self.race_repository)
        self.race_creator_frame = RaceCreatorFrame(self.race_repository)

        self.container.header_menu.menuRequested.connect(self.on_menu_requested)

        self.race_list_frame.race_selected.connect(self.show_race_details)
        
        self.container.set_central(self.race_list_frame)

    def on_menu_requested(self, index: int):
        _, key = self.MENU_ITEMS[index]

        if key == "race_list":
            self.container.set_central(self.race_list_frame)
        elif key == "race_creator":
            self.container.set_central(self.race_creator_frame)

    def show_race_details(self, race):
        self.container.set_central(RaceDetailFrame(self.race_repository,race))