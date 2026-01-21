from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QFrame, QHBoxLayout, QPushButton, QScrollArea, QWidget, QGroupBox, QHeaderView
from PyQt6.QtCore import Qt, QTimer, qFormatLogMessage
from PyQt6.QtGui import QFont, QColor
from backend.db.race_repository import RaceRepository
from backend.db.models import Race

from datetime import datetime
from typing import Sequence, Tuple, List


class RaceDetailFrame(QFrame):
    def __init__(self, race_repository, race, parent=None):
        super().__init__(parent)
        self.race_repository = race_repository
        self.race = race
        
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        
        info_layout = QHBoxLayout()
        self.race_name_label = QLabel(f"Race: {self.race.name}")
        self.race_name_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.race_date_label = QLabel(f"Date: {self.race.date.strftime('%Y-%m-%d')}")
        self.race_date_label.setStyleSheet("font-size: 14px;")
        info_layout.addWidget(self.race_name_label)
        info_layout.addStretch()
        info_layout.addWidget(self.race_date_label)
        main_layout.addLayout(info_layout)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        self.table = QTableWidget()
        self.table.setSortingEnabled(True)
        scroll_area.setWidget(self.table)
        main_layout.addWidget(scroll_area)
        
        self.setMinimumSize(800, 600)
    
    def load_data(self):
        checkpoints = self.race_repository.get_race_checkpoints(self.race)
        checkpoints.sort(key=lambda cp: next(rc.order for rc in self.race.race_checkpoints if rc.checkpoint_id == cp.id))
        
        runners = self.race_repository.get_race_runners(self.race)

        events = self.race_repository.get_race_events(self.race)
        event_map = {(e.runner_id, e.checkpoint_id): e.timestamp for e in events}
        
        n_cols = 3 + len(checkpoints) 
        self.table.setColumnCount(n_cols)
        headers = ["ID", "Name", "Surname"] + [
            cp.name
            for cp in checkpoints
        ]
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(runners))
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        
        for row_idx, runner in enumerate(runners):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(runner.id)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(runner.name))
            self.table.setItem(row_idx, 2, QTableWidgetItem(runner.surname))
            
            all_ts = []
            for col_idx, cp in enumerate(checkpoints, start=3):
                ts = event_map.get((runner.id, cp.id))
                ts_str = ts.strftime("%H:%M:%S.%f")[:-3] if ts else ""
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(ts_str))
                all_ts.append(ts)
            
            if all(all_ts):
                color = QColor(59, 58, 58)
            elif all(ts is None for ts in all_ts):
                color = QColor(56, 48, 48)
            else:
                color = None

            if color:
                for col_idx in range(n_cols):
                    self.table.item(row_idx, col_idx).setBackground(color)