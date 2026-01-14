from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QFrame, QPushButton, QLineEdit, QCheckBox, QMessageBox, QDateEdit, QTimeEdit, QHBoxLayout
from PyQt6.QtCore import QDateTime, QTime, QDate

from backend.db.race_repository import RaceRepository
from backend.db.models import Race
from desktop_ui.config import RACE_CREATOR_INPUT_FIELD_WIDTH

class RaceCreatorFrame(QFrame):
    def __init__(self, race_repository: RaceRepository, parent=None):
        super().__init__(parent)
        self.race_repository = race_repository

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        main_layout.addWidget(QLabel("Race name"))
        name_row = QHBoxLayout()
        self.name_input = QLineEdit()
        self.name_input.setFixedWidth(RACE_CREATOR_INPUT_FIELD_WIDTH)
        self.name_input.setPlaceholderText("Race name")
        name_row.addWidget(self.name_input)
        name_row.addStretch()
        main_layout.addLayout(name_row)

        main_layout.addWidget(QLabel("Race date"))
        date_row = QHBoxLayout()
        self.date_input = QDateEdit(QDate.currentDate())
        self.date_input.setFixedWidth(RACE_CREATOR_INPUT_FIELD_WIDTH)
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        date_row.addWidget(self.date_input)
        date_row.addStretch()
        main_layout.addLayout(date_row)

        main_layout.addWidget(QLabel("Race time"))
        time_row = QHBoxLayout()
        self.time_input = QTimeEdit(QTime.currentTime())
        self.time_input.setFixedWidth(RACE_CREATOR_INPUT_FIELD_WIDTH)
        self.time_input.setDisplayFormat("HH:mm")
        self.time_input.setKeyboardTracking(False)
        time_row.addWidget(self.time_input)
        time_row.addStretch()
        main_layout.addLayout(time_row)

        self.active_checkbox = QCheckBox("Active")
        self.active_checkbox.setChecked(True)
        main_layout.addWidget(self.active_checkbox)

        self.create_button = QPushButton("Create race")
        self.create_button.setFixedWidth(RACE_CREATOR_INPUT_FIELD_WIDTH)
        self.create_button.clicked.connect(self.create_race)
        main_layout.addWidget(self.create_button)

        main_layout.addStretch()

    def create_race(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Validation error", "Race name is required")
            return

        date = self.date_input.date()
        time = self.time_input.time()
        datetime_value = QDateTime(date, time).toPyDateTime()

        race = Race(
            name=name,
            date=datetime_value,
            is_active=self.active_checkbox.isChecked(),
        )

        self.race_repository.add_race(race)

        self.name_input.clear()
        self.active_checkbox.setChecked(True)
