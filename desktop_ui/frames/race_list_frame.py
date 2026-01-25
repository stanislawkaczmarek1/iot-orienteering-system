from typing import List

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QFrame, QMainWindow
from PyQt6.QtCore import Qt

from desktop_ui.config import DATE_FORMAT
from desktop_ui.frames.race_detail_frame import RaceDetailFrame
from desktop_ui.services.race_service import RaceModel, RaceService
from desktop_ui.services.checkpoint_service import CheckpointService
from desktop_ui.services.runner_service import RunnerService
from desktop_ui.services.event_service import EventService
from desktop_ui.content_controller import ContentController


class RaceListFrame(QFrame):
    def __init__(self, content_controller: ContentController, race_service: RaceService,runner_service: RunnerService, event_service: EventService, checkpoint_service: CheckpointService, parent=None):
        super().__init__(parent)
        self.content_controller = content_controller
        self.race_service = race_service
        self.runner_service = runner_service
        self.checkpoint_service = checkpoint_service
        self.event_service = event_service
        self.checkpoint_service = checkpoint_service

        self.init_ui()

        self.race_service.racesLoaded.connect(self.load_races)
        self.race_service.get_races()

    def init_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Races")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Date", "Active"])

        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)

        self.table.cellDoubleClicked.connect(self.on_race_selected)

        layout.addWidget(self.table)


    def on_race_selected(self, row: int, column: int):
        race_id_item = self.table.item(row, 0)
        if not race_id_item:
            return

        race_id = int(race_id_item.text())

        detail_frame = RaceDetailFrame(self.race_service, self.runner_service, self.event_service,self.checkpoint_service, race_id)

        self.content_controller.switch_to_frame(detail_frame)

    def load_races(self, races: List[RaceModel]):
        self.table.setRowCount(len(races))

        for row, race in enumerate(races):
            self.table.setItem(row, 0, QTableWidgetItem(str(race.id)))

            self.table.setItem(row, 1, QTableWidgetItem(race.name))

            date_str = race.date.strftime(DATE_FORMAT)
            self.table.setItem(row, 2, QTableWidgetItem(date_str))

            active_item = QTableWidgetItem("Yes" if race.is_active else "No")
            active_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 3, active_item)

