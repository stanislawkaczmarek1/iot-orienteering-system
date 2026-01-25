from typing import List

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QFrame, QMainWindow, QPushButton, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt

from desktop_ui.config import DATE_FORMAT
from desktop_ui.frames.race_detail_frame import RaceDetailFrame
from desktop_ui.frames.race_creator_frame import RaceCreatorFrame
from desktop_ui.services.race_service import RaceModel, RaceService
from desktop_ui.services.checkpoint_service import CheckpointService
from desktop_ui.services.runner_service import RunnerService
from desktop_ui.services.event_service import EventService
from desktop_ui.content_controller import ContentController


class RaceListFrame(QFrame):
    def __init__(
        self,
        content_controller: ContentController,
        race_service: RaceService,
        runner_service: RunnerService,
        event_service: EventService,
        checkpoint_service: CheckpointService,
        parent=None
    ):
        super().__init__(parent)
        self.content_controller = content_controller
        self.race_service = race_service
        self.runner_service = runner_service
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
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Date", "Active", "Actions"])

        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)

        layout.addWidget(self.table)

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

            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_layout.setSpacing(5)

            view_btn = QPushButton("View")
            edit_btn = QPushButton("Edit")
            delete_btn = QPushButton("Delete")

            view_btn.clicked.connect(lambda _, r_id=race.id: self.view_race(r_id))
            edit_btn.clicked.connect(lambda _, r_id=race.id: self.edit_race(r_id))
            delete_btn.clicked.connect(lambda _, r_id=race.id: self.delete_race(r_id))

            action_layout.addWidget(view_btn)
            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            action_layout.addStretch()

            self.table.setCellWidget(row, 4, action_widget)

    def view_race(self, race_id: int):
        frame = RaceDetailFrame(
            self.race_service,
            self.runner_service,
            self.event_service,
            self.checkpoint_service,
            race_id
        )
        self.content_controller.switch_to_frame(frame)

    def edit_race(self, race_id: int):
        frame = RaceCreatorFrame(
            self.race_service,
            self.checkpoint_service,
        )
        frame.load_race(race_id)
        self.content_controller.switch_to_frame(frame)

    def delete_race(self, race_id: int):
        self.race_service.delete_race(race_id)