
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QStackedWidget, QVBoxLayout, QStackedWidget, QPushButton
from PyQt6.QtCore import pyqtSignal


class HeaderMenuFrame(QFrame):
    menuRequested = pyqtSignal(int)

    def __init__(self, menu_items: list[tuple[str, object]], parent=None):
        super().__init__(parent)

        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFixedHeight(50)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(10)

        self.menu_buttons = []

        for index, (title, _) in enumerate(menu_items):
            btn = QPushButton(title)
            btn.clicked.connect(lambda _, i=index: self.menuRequested.emit(i))
            layout.addWidget(btn)
            self.menu_buttons.append(btn)

        layout.addStretch()

class HeaderMenuPackedFrame(QFrame):
    def __init__(self, menu_items: list[tuple[str, object]], parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.header_menu = HeaderMenuFrame(menu_items)
        self.central_stack = QStackedWidget()

        layout.addWidget(self.header_menu)
        layout.addWidget(self.central_stack)

    def set_central(self, widget: QFrame):
        if self.central_stack.indexOf(widget) == -1:
            self.central_stack.addWidget(widget)
        self.central_stack.setCurrentWidget(widget)