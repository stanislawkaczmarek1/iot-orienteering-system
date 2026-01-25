from typing import Callable

from PyQt6.QtWidgets import QFrame, QWidget, QHBoxLayout, QPushButton, QStackedLayout

from desktop_ui.content_controller import ContentController

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
    def __init__(self, menu_items: list[tuple[str, Callable]], content_controller: ContentController,parent=None):
        super().__init__(parent)
        self.setFixedHeight(50)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.menu_buttons = []
        self.menu_factories = []
        self.menu_frames = []

        for index, (title, frame_factory) in enumerate(menu_items):
            btn = HeaderMenuButton(title)
            layout.addWidget(btn)
            # Connect to parent controller if exists
            btn.clicked.connect(lambda _, i=index: content_controller.switch_to_index(i))
            self.menu_buttons.append(btn)
            self.menu_factories.append(frame_factory)
            self.menu_frames.append(None)

        layout.addStretch()

    def get_frame(self, index: int) -> QWidget:
        if self.menu_frames[index] is None:
            factory = self.menu_factories[index]
            self.menu_frames[index] = factory() if callable(factory) else factory
        return self.menu_frames[index]

    def set_active(self, index: int):
        for i, btn in enumerate(self.menu_buttons):
            btn.set_active(i == index)
