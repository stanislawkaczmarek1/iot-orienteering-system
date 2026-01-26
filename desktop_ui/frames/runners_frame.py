from typing import List

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QLabel, QTableWidget, QHeaderView, 
    QWidget, QHBoxLayout, QPushButton, QAbstractItemView, 
    QTableWidgetItem, QInputDialog, QDialog, QFormLayout, QLineEdit, QDialogButtonBox
)

from desktop_ui.services.runner_service import RunnerService, RunnerModel


class AddRunnerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Runner")
        self.setModal(True)
        self.setMinimumWidth(300)

        layout = QFormLayout(self)

        self.rfid_input = QLineEdit()
        self.rfid_input.setPlaceholderText("Enter RFID UID")
        layout.addRow("RFID UID:", self.rfid_input)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter name (optional)")
        layout.addRow("Name:", self.name_input)

        self.surname_input = QLineEdit()
        self.surname_input.setPlaceholderText("Enter surname (optional)")
        layout.addRow("Surname:", self.surname_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_values(self):
        return {
            "rfid_uid": self.rfid_input.text(),
            "name": self.name_input.text(),
            "surname": self.surname_input.text()
        }


class RunnersFrame(QFrame):
    HEADERS = ["ID", "RFID UID", "Name", "Surname", "Actions"]

    def __init__(self, runner_service: RunnerService, parent=None):
        super().__init__(parent)
        self.runner_service = runner_service
        self.runners: List[RunnerModel] = []

        self.table = QTableWidget(self)
        self.table.setColumnCount(len(self.HEADERS))
        self.table.setHorizontalHeaderLabels(self.HEADERS)

        self.init_ui()

        self.runner_service.runnersLoaded.connect(self.update_runners)
        self.runner_service.get_runners()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Title and Add button row
        title_row = QHBoxLayout()
        
        title = QLabel("Runners")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_row.addWidget(title)

        title_row.addStretch()

        add_button = QPushButton("Add Runner")
        add_button.setFixedSize(120, 30)
        add_button.clicked.connect(self.on_add_runner)
        title_row.addWidget(add_button)

        layout.addLayout(title_row)

        # Table setup
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.verticalHeader().setVisible(False)

        layout.addWidget(self.table)

    def update_runners(self, runners: list[RunnerModel]):
        self.runners = runners
        self.table.setRowCount(len(runners))
        self.draw_table()

    def draw_table(self):
        for row, runner in enumerate(self.runners):
            id_item = QTableWidgetItem(str(runner.id))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, id_item)

            rfid_item = QTableWidgetItem(str(runner.rfid_uid))
            rfid_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 1, rfid_item)

            self.table.setItem(row, 2, QTableWidgetItem(runner.name))
            self.table.setItem(row, 3, QTableWidgetItem(runner.surname))

            # Action buttons
            edit_button = QPushButton("Edit")
            edit_button.setFixedSize(70, 25)
            edit_button.clicked.connect(lambda _, r=runner: self.on_edit(r))

            delete_button = QPushButton("Delete")
            delete_button.setFixedSize(70, 25)
            delete_button.clicked.connect(lambda _, rid=runner.id: self.on_delete(rid))

            container = QWidget()
            layout = QHBoxLayout(container)
            layout.setContentsMargins(4, 0, 4, 0)
            layout.setAlignment(Qt.AlignmentFlag.AlignRight)
            layout.addWidget(edit_button)
            layout.addWidget(delete_button)

            self.table.setCellWidget(row, 4, container)

        self.table.resizeColumnToContents(0)
        self.table.resizeColumnToContents(1)
        self.table.resizeColumnToContents(4)

    def on_add_runner(self):
        dialog = AddRunnerDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            values = dialog.get_values()
            rfid_uid = values["rfid_uid"]
            
            if not rfid_uid:
                return
            
            try:
                rfid_uid_int = int(rfid_uid)
                self.runner_service.create_runner(
                    rfid_uid_int, 
                    values["name"] or "", 
                    values["surname"] or ""
                )
            except ValueError:
                print(f"Invalid RFID UID: {rfid_uid}")

    def on_delete(self, runner_id: int):
        self.runner_service.delete_runner(runner_id)

    def on_edit(self, runner: RunnerModel):
        # Create a dialog with name and surname fields
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Runner")
        dialog.setModal(True)
        dialog.setMinimumWidth(300)

        layout = QFormLayout(dialog)

        name_input = QLineEdit(runner.name)
        layout.addRow("Name:", name_input)

        surname_input = QLineEdit(runner.surname)
        layout.addRow("Surname:", surname_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_name = name_input.text()
            new_surname = surname_input.text()
            
            if new_name != runner.name or new_surname != runner.surname:
                self.runner_service.update_runner_name(runner.id, new_name, new_surname)
