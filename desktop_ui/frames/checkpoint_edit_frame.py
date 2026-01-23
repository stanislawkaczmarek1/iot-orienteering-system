from typing import List

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt, pyqtSignal, QEvent
from PyQt6.QtWidgets import QFrame, QTableView, QVBoxLayout, QLabel, QTableWidget, QStyledItemDelegate, \
    QStyleOptionButton, QStyle, QHeaderView, QWidget, QHBoxLayout, QPushButton, QAbstractItemView, QTableWidgetItem, \
    QInputDialog

from desktop_ui.services.checkpoint_service import CheckpointService, CheckpointModel



class CheckpointsListFrame(QFrame):
    HEADERS = ["ID", "Name", "UUID", ""]

    def __init__(self, checkpoint_service: CheckpointService, parent=None):
        super().__init__(parent)
        self.checkpoint_service = checkpoint_service
        self.checkpoints: List[CheckpointModel] = []

        self.table = QTableWidget(self)
        self.table.setColumnCount(len(self.HEADERS))
        self.table.setHorizontalHeaderLabels(self.HEADERS)

        self.init_ui()

        self.checkpoint_service.checkpointsLoaded.connect(self.update_checkpoints)
        self.checkpoint_service.get_checkpoints()

    def init_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Checkpoints")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        # header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.verticalHeader().setVisible(False)

        layout.addWidget(self.table)

    def update_checkpoints(self, checkpoints: list[CheckpointModel]):
        self.checkpoints = checkpoints
        self.table.setRowCount(len(checkpoints))
        self.draw_table()

    def draw_table(self):
        for row, checkpoint in enumerate(self.checkpoints):
            id_item = QTableWidgetItem(str(checkpoint.id))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row, 0, id_item)

            name_item = QTableWidgetItem(checkpoint.name)
            self.table.setItem(row, 1, name_item)

            self.table.setItem(row, 2, QTableWidgetItem(str(checkpoint.uuid)))

            d_button = QPushButton("Delete")
            d_button.setFixedSize(70, 25)
            d_button.clicked.connect(lambda _, cid=checkpoint.id: self.on_delete(cid))

            e_button = QPushButton("Rename")
            e_button.setFixedSize(70, 25)
            e_button.clicked.connect(lambda _, c=checkpoint: self.on_edit(c))

            container = QWidget()
            layout = QHBoxLayout(container)
            layout.setContentsMargins(4, 0, 4, 0)
            layout.setAlignment(Qt.AlignmentFlag.AlignRight)
            layout.addWidget(e_button)
            layout.addWidget(d_button)

            self.table.setCellWidget(row, 3, container)

        self.table.resizeColumnToContents(0)
        self.table.resizeColumnToContents(3)


    def on_delete(self, id: int):
        print(f"on_delete {id}")
        self.checkpoint_service.delete_checkpoint(id)

    def on_edit(self, checkpoint: CheckpointModel):
        new_name, ok = QInputDialog.getText(
            self, "Edit Name", "New name:", text=checkpoint.name
        )

        if ok and new_name and new_name != checkpoint.name:
            self.checkpoint_service.update_checkpoint_name(checkpoint.id, new_name)
