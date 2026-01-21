from typing import List

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QFrame
from PyQt6.QtCore import Qt

from desktop_ui.config import DATE_FORMAT
from desktop_ui.services.race_service import RaceService, RaceModel


class RaceListFrame(QFrame):
    def __init__(self, race_service: RaceService, parent=None):
        super().__init__(parent)
        self.race_service = race_service

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

