from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QFrame
from PyQt6.QtCore import Qt, pyqtSignal

from desktop_ui.config import DATE_FORMAT
from backend.db.race_repository import RaceRepository

class RaceListFrame(QFrame):

    race_selected = pyqtSignal(object) 

    def __init__(self, race_repository: RaceRepository, parent=None):
        super().__init__(parent)
        self.race_repository = race_repository

        self.init_ui()
        self.load_races()

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

        self.table.cellClicked.connect(self.on_row_clicked)

        layout.addWidget(self.table)


    def load_races(self):
        self.races = self.race_repository.get_races()
        self.table.setRowCount(len(self.races))

        for row, race in enumerate(self.races):
            id_item = QTableWidgetItem(str(race.id))
            id_item.setData(Qt.ItemDataRole.UserRole, race)
            self.table.setItem(row, 0, id_item)
            
            self.table.setItem(row, 1, QTableWidgetItem(race.name))

            date_str = race.date.strftime(DATE_FORMAT)
            self.table.setItem(row, 2, QTableWidgetItem(date_str))

            active_item = QTableWidgetItem("Yes" if race.is_active else "No")
            active_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 3, active_item)

        self.table.resizeColumnsToContents()

    def on_row_clicked(self, row, column):
        race_item = self.table.item(row, 0)
        if race_item:
            race = race_item.data(Qt.ItemDataRole.UserRole)
            self.race_selected.emit(race)
