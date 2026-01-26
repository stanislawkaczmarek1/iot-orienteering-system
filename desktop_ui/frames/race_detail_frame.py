from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, 
    QHBoxLayout, QPushButton, QWidget, QHeaderView, QDialog, 
    QListWidget, QListWidgetItem, QDialogButtonBox, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtGui import QColor
from datetime import datetime

from desktop_ui.services.race_service import RaceModel, RaceService
from desktop_ui.services.checkpoint_service import CheckpointService, CheckpointModel
from desktop_ui.services.runner_service import RunnerService, RunnerModel
from desktop_ui.services.event_service import EventService


class AddRunnerToRaceDialog(QDialog):
    def __init__(self, all_runners: list[RunnerModel], race_runners: list[RunnerModel], parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Runner to Race")
        self.setModal(True)
        self.setMinimumSize(400, 300)

        # Filter out runners already in the race
        race_runner_ids = {r.id for r in race_runners}
        self.available_runners = [r for r in all_runners if r.id not in race_runner_ids]

        layout = QVBoxLayout(self)

        label = QLabel("Select runners to add to this race:")
        layout.addWidget(label)

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        
        for runner in self.available_runners:
            item_text = f"{runner.name} {runner.surname} (RFID: {runner.rfid_uid})"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, runner.id)
            self.list_widget.addItem(item)
        
        layout.addWidget(self.list_widget)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_selected_runner_ids(self) -> list[int]:
        selected_ids = []
        for item in self.list_widget.selectedItems():
            runner_id = item.data(Qt.ItemDataRole.UserRole)
            selected_ids.append(runner_id)
        return selected_ids


class RaceDetailViewModel(QObject):
    data_updated = pyqtSignal()

    def __init__(self, race_service: RaceService, runner_service: RunnerService, event_service: EventService, checkpoint_service: CheckpointService, race_id: int):
        super().__init__()
        self.race_service = race_service
        self.runner_service = runner_service
        self.event_service = event_service
        self.checkpoint_service = checkpoint_service
        self.race_id = race_id

        self.race: RaceModel | None = None
        self.runners: list[RunnerModel] = []
        self.checkpoints: list[CheckpointModel] = []
        self.events_map: dict[tuple[int, int], datetime] = {}  # (runner_id, checkpoint_id) -> timestamp

        self._load_race()
        self._load_checkpoints()
        self._load_runners()
        self._load_events()

    def _load_race(self):
        def handle_callback(race):
            self.race = race
            self.data_updated.emit()
        self.race_service.get_race_by_id(self.race_id, handle_callback)

    def _load_checkpoints(self):
        def handle_checkpoints(checkpoints):
            self.checkpoints = sorted(checkpoints, key=lambda cp: getattr(cp, "order", 0))
            self.data_updated.emit()

        self.checkpoint_service.get_checkpoints_of_race(self.race_id, handle_checkpoints)

    def _load_runners(self):
        def handle_callback(runners):
            self.runners = runners
            self.data_updated.emit()

        self.runner_service.get_runners_of_race(self.race_id, handle_callback)

    def _load_events(self):
        def handle_callback(events):
            self.events_map = {}
            for e in events:
                ts = (
                    datetime.fromisoformat(e.timestamp)
                    if isinstance(e.timestamp, str)
                    else e.timestamp
                )

                key = (e.runner_id, e.checkpoint_id)
                self.events_map[key] = ts

            self.data_updated.emit()

        self.event_service.get_events_of_race(self.race_id, handle_callback)

    def refresh(self):
        self._load_race()
        self._load_checkpoints()
        self._load_runners()


class RaceDetailFrame(QFrame):
    def __init__(self, race_service: RaceService, runner_service: RunnerService, event_service: EventService, checkpoint_service: CheckpointService, race_id: int, parent=None):
        super().__init__(parent)
        self.race_service = race_service
        self.runner_service = runner_service
        self.view_model = RaceDetailViewModel( race_service, runner_service, event_service, checkpoint_service, race_id )
        self.all_runners: list[RunnerModel] = []

        self.init_ui()
        self.view_model.data_updated.connect(self.load_data)
        
        # Load all runners for the add dialog
        self.runner_service.runnersLoaded.connect(self.on_all_runners_loaded)

    def on_all_runners_loaded(self, runners: list[RunnerModel]):
        self.all_runners = runners

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Header with race info and add runner button
        header_layout = QHBoxLayout()
        
        info_layout = QVBoxLayout()
        self.race_name_label = QLabel("Race: ")
        self.race_date_label = QLabel("Date: ")
        info_layout.addWidget(self.race_name_label)
        info_layout.addWidget(self.race_date_label)
        header_layout.addLayout(info_layout)
        
        header_layout.addStretch()
        
        self.add_runner_btn = QPushButton("Add Runner to Race")
        self.add_runner_btn.setFixedSize(150, 30)
        self.add_runner_btn.clicked.connect(self.on_add_runner_clicked)
        header_layout.addWidget(self.add_runner_btn)
        
        layout.addLayout(header_layout)

        self.table = QTableWidget()
        layout.addWidget(self.table)

    def load_data(self):
        vm = self.view_model

        if vm.race is not None:
            self.race_name_label.setText(f"Race: {vm.race.name}")
            self.race_date_label.setText(
                f"Date: {vm.race.date.strftime('%Y-%m-%d')}"
            )

        n_cols = 4 + len(vm.checkpoints)  # Added 1 for Actions column
        self.table.setColumnCount(n_cols)

        headers = ["ID", "Name", "Surname"] + [cp.name for cp in vm.checkpoints] + ["Actions"]
        self.table.setHorizontalHeaderLabels(headers)

        self.table.setRowCount(len(vm.runners))
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(False)  # Disable sorting to avoid issues with widgets

        event_map = vm.events_map

        for row_idx, runner in enumerate(vm.runners):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(runner.id)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(runner.name))
            self.table.setItem(row_idx, 2, QTableWidgetItem(runner.surname))

            all_ts = []

            for col_idx, cp in enumerate(vm.checkpoints, start=3):
                ts = event_map.get((runner.id, cp.id))
                ts_str = ts.strftime("%H:%M:%S.%f")[:-3] if ts else ""
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(ts_str))
                all_ts.append(ts)

            # Add remove button in the last column
            remove_btn = QPushButton("Remove")
            remove_btn.setFixedSize(70, 25)
            remove_btn.clicked.connect(lambda _, rid=runner.id: self.on_remove_runner(rid))
            
            container = QWidget()
            btn_layout = QHBoxLayout(container)
            btn_layout.setContentsMargins(4, 0, 4, 0)
            btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            btn_layout.addWidget(remove_btn)
            
            self.table.setCellWidget(row_idx, n_cols - 1, container)

            # row coloring
            if all(all_ts):
                color = QColor(59, 58, 58)
            elif all(ts is None for ts in all_ts):
                color = QColor(56, 48, 48)
            else:
                color = None

            if color:
                for col_idx in range(n_cols - 1):  # Exclude actions column
                    item = self.table.item(row_idx, col_idx)
                    if item:
                        item.setBackground(color)

    def on_add_runner_clicked(self):
        if not self.all_runners:
            QMessageBox.warning(self, "No Runners", "No runners available. Please create runners first.")
            return
        
        dialog = AddRunnerToRaceDialog(self.all_runners, self.view_model.runners, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_ids = dialog.get_selected_runner_ids()
            if selected_ids:
                for runner_id in selected_ids:
                    self.race_service.add_runner_to_race(
                        self.view_model.race_id, 
                        runner_id,
                        lambda success: self.on_runner_added(success)
                    )

    def on_runner_added(self, success: bool):
        if success:
            # Refresh the runners list
            self.view_model._load_runners()
        else:
            QMessageBox.warning(self, "Error", "Failed to add runner to race.")

    def on_remove_runner(self, runner_id: int):
        reply = QMessageBox.question(
            self, 
            "Confirm Removal",
            "Are you sure you want to remove this runner from the race?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.race_service.remove_runner_from_race(
                self.view_model.race_id,
                runner_id,
                lambda success: self.on_runner_removed(success)
            )

    def on_runner_removed(self, success: bool):
        if success:
            # Refresh the runners list
            self.view_model._load_runners()
        else:
            QMessageBox.warning(self, "Error", "Failed to remove runner from race.")