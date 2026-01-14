
from PyQt6.QtWidgets import QFrame, QWidget, QHBoxLayout, QPushButton, QStackedLayout


class HeaderMenuFrame(QFrame):
    def __init__(self, menu_items: list[tuple[str, "QFrame | callable"]], parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFixedHeight(50)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(10)
        
        self.menu_buttons = []
        self.menu_factories = []
        self.menu_frames = []
        
        self.stacked_layout = QStackedLayout()
        self.stacked_widget = QWidget()
        self.stacked_widget.setLayout(self.stacked_layout)
        
        for index, (title, frame_or_factory) in enumerate(menu_items):
            btn = QPushButton(title)
            layout.addWidget(btn)
            btn.clicked.connect(lambda _, i=index: self.switch_to(i))
            self.menu_buttons.append(btn)
            self.menu_factories.append(frame_or_factory)
            self.menu_frames.append(None)
        
        layout.addStretch()
    

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
