from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QFrame, QPushButton, QLineEdit, QCheckBox, QMessageBox, QDateEdit, QTimeEdit, QHBoxLayout, QListWidget, QAbstractItemView, QListWidgetItem
from PyQt6.QtCore import QDateTime, QTime, QDate, Qt

from desktop_ui.config import RACE_CREATOR_INPUT_FIELD_WIDTH
from desktop_ui.content_controller import ContentController
from desktop_ui.services.race_service import RaceService
from desktop_ui.services.checkpoint_service import CheckpointService

class RaceCreatorFrame(QFrame):
    def __init__(self, content_controller: ContentController, race_service: RaceService, checkpoint_service: CheckpointService, parent=None):
        super().__init__(parent)
        self.content_controller = content_controller
        self.race_service = race_service
        self.checkpoint_service = checkpoint_service
        self.editing_race_id = None
        self.init_ui()
        self.load_checkpoints()

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

        main_layout.addWidget(QLabel("Available Checkpoints"))
        checkpoints_layout = QHBoxLayout()
        self.available_checkpoints_list = QListWidget()
        self.available_checkpoints_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        checkpoints_layout.addWidget(self.available_checkpoints_list)

        self.selected_checkpoints_list = QListWidget()
        self.selected_checkpoints_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.selected_checkpoints_list.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        checkpoints_layout.addWidget(self.selected_checkpoints_list)

        buttons_layout = QVBoxLayout()
        self.add_checkpoint_button = QPushButton("→")
        self.add_checkpoint_button.clicked.connect(self.add_selected_checkpoint)
        self.remove_checkpoint_button = QPushButton("←")
        self.remove_checkpoint_button.clicked.connect(self.remove_selected_checkpoint)
        self.move_up_button = QPushButton("↑")
        self.move_up_button.clicked.connect(lambda: self.move_checkpoint(-1))
        self.move_down_button = QPushButton("↓")
        self.move_down_button.clicked.connect(lambda: self.move_checkpoint(1))
        for btn in [self.add_checkpoint_button, self.remove_checkpoint_button, self.move_up_button, self.move_down_button]:
            buttons_layout.addWidget(btn)
        buttons_layout.addStretch()
        checkpoints_layout.addLayout(buttons_layout)

        main_layout.addLayout(checkpoints_layout)

        self.create_button = QPushButton("Create race")
        self.create_button.setFixedWidth(RACE_CREATOR_INPUT_FIELD_WIDTH)
        self.create_button.clicked.connect(self.save_race)
        main_layout.addWidget(self.create_button)

        main_layout.addStretch()

    def load_checkpoints(self):
        def on_loaded(checkpoints):
            self.populate_checkpoints(checkpoints)
            self.checkpoint_service.checkpointsLoaded.disconnect(on_loaded)

        self.checkpoint_service.checkpointsLoaded.connect(on_loaded)
        self.checkpoint_service.get_checkpoints()


    def populate_checkpoints(self, checkpoints):
        selected_ids = set(
            self.selected_checkpoints_list.item(i).data(Qt.ItemDataRole.UserRole)
            for i in range(self.selected_checkpoints_list.count())
        )

        self.available_checkpoints_list.clear()
        for cp in checkpoints:
            item = QListWidgetItem(f"{cp.id}: {cp.name}")
            item.setData(Qt.ItemDataRole.UserRole, cp.id)
            self.available_checkpoints_list.addItem(item)

        for i in range(self.available_checkpoints_list.count()):
            item = self.available_checkpoints_list.item(i)
            if item.data(Qt.ItemDataRole.UserRole) in selected_ids:
                item.setSelected(True)


    def add_selected_checkpoint(self):
        for item in self.available_checkpoints_list.selectedItems():
            cp_id = item.data(Qt.ItemDataRole.UserRole)
            if not any(self.selected_checkpoints_list.item(i).data(Qt.ItemDataRole.UserRole) == cp_id
                    for i in range(self.selected_checkpoints_list.count())):
                new_item = QListWidgetItem(item.text())
                new_item.setData(Qt.ItemDataRole.UserRole, cp_id)
                self.selected_checkpoints_list.addItem(new_item)


    def remove_selected_checkpoint(self):
        for item in self.selected_checkpoints_list.selectedItems():
            self.selected_checkpoints_list.takeItem(self.selected_checkpoints_list.row(item))

    def move_checkpoint(self, direction):
        row = self.selected_checkpoints_list.currentRow()
        if row < 0:
            return
        new_row = row + direction
        if new_row < 0 or new_row >= self.selected_checkpoints_list.count():
            return
        item = self.selected_checkpoints_list.takeItem(row)
        self.selected_checkpoints_list.insertItem(new_row, item)
        self.selected_checkpoints_list.setCurrentRow(new_row)
        self.selected_checkpoints_list.setFocus() 

    def load_race(self, race_id):
        def populate(race):
            self.editing_race_id = race_id
            self.name_input.setText(race.name)
            self.location_input.setText(race.location)
            dt = QDateTime(QDate(race.date.year, race.date.month, race.date.day),
                           QTime(race.date.hour, race.date.minute, race.date.second))
            self.date_input.setDate(dt.date())
            self.time_input.setTime(dt.time())
            self.active_checkbox.setChecked(race.is_active)
            self.create_button.setText("Save changes")

            self.checkpoint_service.get_checkpoints_of_race(race_id, self.populate_selected_checkpoints)
        self.race_service.get_race_by_id(race_id, populate)

    def populate_selected_checkpoints(self, checkpoints):
        self.selected_checkpoints_list.clear()

        for cp in checkpoints:
            item = QListWidgetItem(f"{cp.id}: {cp.name}")
            item.setData(Qt.ItemDataRole.UserRole, cp.id)
            self.selected_checkpoints_list.addItem(item)

        
    def _reset_form(self):
        self.editing_race_id = None
        self.name_input.clear()
        self.location_input.clear()
        self.date_input.setDate(QDate.currentDate())
        self.time_input.setTime(QTime.currentTime())
        self.active_checkbox.setChecked(True)
        self.create_button.setText("Create race")
        self.selected_checkpoints_list.clear()

    def save_race(self):
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

        race_data = {
            "name": name,
            "location": location,
            "date": datetime_value.isoformat(),
            "is_active": self.active_checkbox.isChecked(),
        }

        if self.editing_race_id:
            self.race_service.update_race(self.editing_race_id, race_data)
            race_id = self.editing_race_id
            selected_checkpoint_ids = [
                self.selected_checkpoints_list.item(i).data(Qt.ItemDataRole.UserRole)
                for i in range(self.selected_checkpoints_list.count())
            ]
            if selected_checkpoint_ids:
                self.checkpoint_service.replace_race_checkpoints(race_id, selected_checkpoint_ids, self._reset_form())

            self.content_controller.switch_to_index(1)  # switch to race list

        else:
            def on_race_created(data):
                race_id = data.get("id")

                selected_checkpoint_ids = [
                    self.selected_checkpoints_list.item(i).data(Qt.ItemDataRole.UserRole)
                    for i in range(self.selected_checkpoints_list.count())
                ]

                if selected_checkpoint_ids:
                    self.checkpoint_service.add_checkpoints_to_race(race_id, selected_checkpoint_ids, self._reset_form())

            self.race_service.raceCreated.connect(on_race_created)
            self.race_service.create_race(race_data)
