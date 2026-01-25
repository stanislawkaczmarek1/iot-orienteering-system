from PyQt6.QtWidgets import QMainWindow, QFrame, QVBoxLayout, QStackedLayout, QWidget
from sqlalchemy.orm import Session

from desktop_ui.frames.checkpoint_edit_frame import CheckpointsListFrame
from desktop_ui.frames.dashboard_frame import DashboardFrame
from desktop_ui.frames.race_list_frame import RaceListFrame
from desktop_ui.frames.race_creator_frame import RaceCreatorFrame
from desktop_ui.frames.header_menu_frame import HeaderMenuFrame
from desktop_ui.content_controller import ContentController

from desktop_ui.config import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT
from desktop_ui.services.checkpoint_service import CheckpointService
from desktop_ui.services.race_service import RaceService
from desktop_ui.services.event_service import EventService
from desktop_ui.services.runner_service import RunnerService

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.race_service = RaceService()
        self.checkpoint_service = CheckpointService()
        self.event_service = EventService()
        self.runner_service = RunnerService()

        self.content_area = QStackedLayout()
        self.content_widget = QWidget()
        self.content_widget.setLayout(self.content_area)

        self.content_controller = ContentController(self.content_area, None)

        self.menu_items = [
            ("Dashboard", lambda: DashboardFrame(self.content_controller,self.race_service)),
            ("Race List", lambda: RaceListFrame(self.content_controller, self.race_service, self.runner_service, self.event_service, self.checkpoint_service)),
            ("Race Creator", lambda: RaceCreatorFrame(self.race_service)),
            ("Checkpoints", lambda: CheckpointsListFrame(self.checkpoint_service)),
        ]

        self.header_menu = HeaderMenuFrame(self.menu_items, self.content_controller, self)
        self.content_controller.header_menu = self.header_menu 

        self.setWindowTitle(WINDOW_TITLE)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Main layout
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)
        central_widget.setLayout(central_layout)

        central_layout.addWidget(self.header_menu)
        central_layout.addWidget(self.content_widget)
        self.setCentralWidget(central_widget)

        # Show initial frame
        self.content_controller.switch_to_index(0)

