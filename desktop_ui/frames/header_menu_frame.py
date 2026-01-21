from typing import Callable

from PyQt6.QtWidgets import QFrame, QWidget, QHBoxLayout, QPushButton, QStackedLayout

class HeaderMenuButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

        self.setStyleSheet("""
            QPushButton {
                background-color: #343a40;
                border: none;
                border-right: 1px solid #495057;
                padding: 4px 8px;
                height: 100%;
                width: 120px;
            }
            
            QPushButton:hover {
                background-color: #495057;
            }
            
            QPushButton[active = "true"] {
                background-color: #212529;
            }
        """)

    def set_active(self, active: bool):
        self.setProperty("active", "true" if active else "false")
        self.style().unpolish(self)
        self.style().polish(self)




class HeaderMenuFrame(QFrame):
    def __init__(self, menu_items: list[tuple[str, QFrame | Callable]], parent=None):
        super().__init__(parent)
        # self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFixedHeight(50)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.menu_buttons = []
        self.menu_factories = []
        self.menu_frames = []

        self.stacked_layout = QStackedLayout()
        self.stacked_widget = QWidget()
        self.stacked_widget.setLayout(self.stacked_layout)

        for index, (title, frame_or_factory) in enumerate(menu_items):
            btn = HeaderMenuButton(title)
            layout.addWidget(btn)
            btn.clicked.connect(lambda _, i=index: self.switch_to(i))
            self.menu_buttons.append(btn)
            self.menu_factories.append(frame_or_factory)
            self.menu_frames.append(None)

        layout.addStretch()

        self.switch_to(0)

    def switch_to(self, index: int):
        if self.menu_frames[index] is None:
            factory = self.menu_factories[index]
            if callable(factory):
                frame = factory()
            else:
                frame = factory
            self.menu_frames[index] = frame
            self.stacked_layout.addWidget(frame)
        self.stacked_layout.setCurrentWidget(self.menu_frames[index])
        for i, btn in enumerate(self.menu_buttons):
            btn.set_active(index == i)
