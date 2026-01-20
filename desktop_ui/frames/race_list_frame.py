from typing import List

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QFrame, QTableView
from desktop_ui.config import DATE_FORMAT
from desktop_ui.services.race_service import RaceService, RaceModel
from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex, QTimer


class RaceListModel(QAbstractTableModel):
    HEADERS = ["Name", "Date", "Location"]

    def __init__(self, race_service: RaceService, parent=None):
        super().__init__(parent)
        self.race_service = race_service
        self._races: List[RaceModel] = []

        self.race_service.racesLoaded.connect(self.on_races_loaded)
        self.race_service.get_races()

    def on_races_loaded(self, races):
        self.beginResetModel()
        self._races = races
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        return len(self._races)

    def columnCount(self, parent=QModelIndex()):
        return len(self.HEADERS)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None
        race = self._races[index.row()]
        if index.column() == 0:
            return race.name
        elif index.column() == 1:
            return race.date.strftime(DATE_FORMAT)
        elif index.column() == 2:
            return race.location

    def headerData(self, section, orientation, role):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.HEADERS[section]


class RaceListFrame(QFrame):
    def __init__(self, race_service: RaceService, parent=None):
        super().__init__(parent)
        self.race_service = race_service

        self.model = RaceListModel(race_service, self)
        self.table = QTableView()
        self.table.setModel(self.model)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Races")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)

        layout.addWidget(self.table)
