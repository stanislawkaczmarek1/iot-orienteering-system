from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QFrame, QPushButton, QLineEdit, QCheckBox, QMessageBox, QDateEdit, QTimeEdit, QHBoxLayout
from PyQt6.QtCore import QDateTime, QTime, QDate

from desktop_ui.config import RACE_CREATOR_INPUT_FIELD_WIDTH
from desktop_ui.services.race_service import RaceService


class RaceCreatorFrame(QFrame):
    def __init__(self, race_service: RaceService, parent=None):
        super().__init__(parent)
        self.race_service = race_service

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

        main_layout.addWidget(QLabel("Race location"))
        location_row = QHBoxLayout()
        self.location_input = QLineEdit()
        self.location_input.setFixedWidth(RACE_CREATOR_INPUT_FIELD_WIDTH)
        self.location_input.setPlaceholderText("Race location")
        location_row.addWidget(self.location_input)
        location_row.addStretch()
        main_layout.addLayout(location_row)


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

        location = self.location_input.text().strip()
        if not location:
            QMessageBox.warning(self, "Validation error", "Race location is required")
            return

        date = self.date_input.date()
        time = self.time_input.time()
        datetime_value = QDateTime(date, time).toPyDateTime()

        self.race_service.create_race({
            "name": name,
            "location": location,
            "date": datetime_value.isoformat(),
            "is_active": self.active_checkbox.isChecked(),
        })

        self.name_input.clear()
        self.location_input.clear()
        self.date_input.setDate(QDate.currentDate())
        self.time_input.setTime(QTime.currentTime())

        self.active_checkbox.setChecked(True)
