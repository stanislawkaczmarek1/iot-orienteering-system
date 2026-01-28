from PyQt6.QtWidgets import QStackedLayout, QWidget 

class ContentController:
    def __init__(self, content_area: QStackedLayout, header_menu: 'HeaderMenuFrame'):
        self.content_area = content_area
        self.header_menu = header_menu

    def switch_to_index(self, index: int):
        frame = self.header_menu.get_frame(index)
        self._show_frame(frame)
        self.header_menu.set_active(index)

    def switch_to_frame(self, frame: QWidget):
        self._show_frame(frame)

    def _show_frame(self, frame: QWidget):
        if self.content_area.indexOf(frame) == -1:
            self.content_area.addWidget(frame)
        self.content_area.setCurrentWidget(frame)
