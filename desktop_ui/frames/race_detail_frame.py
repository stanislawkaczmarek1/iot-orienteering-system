from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QFrame, QHBoxLayout, QPushButton, QScrollArea, QWidget, QGroupBox, QHeaderView
from PyQt6.QtCore import Qt, QTimer, qFormatLogMessage, pyqtSignal, QObject
from PyQt6.QtGui import QFont, QColor
from datetime import datetime

from desktop_ui.services.race_service import RaceModel, RaceService
from desktop_ui.services.checkpoint_service import CheckpointService, CheckpointModel
from desktop_ui.services.runner_service import RunnerService, RunnerModel
from desktop_ui.services.event_service import EventService

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
            self.checkpoints = checkpoints
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
        self.view_model = RaceDetailViewModel( race_service, runner_service, event_service, checkpoint_service, race_id )

        self.init_ui()
        self.view_model.data_updated.connect(self.load_data)

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.race_name_label = QLabel("Race: ")
        self.race_date_label = QLabel("Date: ")

        layout.addWidget(self.race_name_label)
        layout.addWidget(self.race_date_label)

        self.table = QTableWidget()
        layout.addWidget(self.table)

    def load_data(self):
        vm = self.view_model

        if vm.race is not None:
            self.race_name_label.setText(f"Race: {vm.race.name}")
            self.race_date_label.setText(
                f"Date: {vm.race.date.strftime('%Y-%m-%d')}"
            )

        n_cols = 3 + len(vm.checkpoints)
        self.table.setColumnCount(n_cols)

        headers = ["ID", "Name", "Surname"] + [cp.name for cp in vm.checkpoints]
        self.table.setHorizontalHeaderLabels(headers)

        self.table.setRowCount(len(vm.runners))
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)

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

            # row coloring
            if all(all_ts):
                color = QColor(59, 58, 58)
            elif all(ts is None for ts in all_ts):
                color = QColor(56, 48, 48)
            else:
                color = None

            if color:
                for col_idx in range(n_cols):
                    item = self.table.item(row_idx, col_idx)
                    if item:
                        item.setBackground(color)