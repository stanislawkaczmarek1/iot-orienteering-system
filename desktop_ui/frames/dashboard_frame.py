from typing import List, Callable

from PyQt6.QtCore import Qt, QObject, pyqtSignal
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout, QPushButton

from desktop_ui.frames.race_detail_frame import RaceDetailFrame
from desktop_ui.services.checkpoint_service import CheckpointService
from desktop_ui.services.event_service import EventService
from desktop_ui.services.race_service import RaceModel, RaceService
from desktop_ui.content_controller import ContentController
from desktop_ui.services.runner_service import RunnerService

CARD_WIDTH = 150
CARD_HEIGHT = 130


class DashboardViewModel(QObject):
    dashboard_updated = pyqtSignal()

    def __init__(self, race_service: RaceService):
        super().__init__()
        self._card_width = CARD_WIDTH
        self._view_width = 800

        self.incoming_races = []
        self.historic_races = []

        self.visible_incoming = []
        self.visible_historic = []

        race_service.racesLoaded.connect(self.on_data_received)
        race_service.get_races()

    def on_data_received(self, all_races: List[RaceModel]):
        self.incoming_races = list(filter(lambda x: x.is_active, all_races))
        self.historic_races = list(filter(lambda x: not x.is_active, all_races))
        self._recalc_visible_cards()

    def update_width(self, width):
        self._view_width = width
        self._recalc_visible_cards()

    def _recalc_visible_cards(self):
        padding = 20
        available_width = max(1, self._view_width - padding)
        max_items = max(1, available_width // self._card_width)

        self.visible_incoming = self.incoming_races[:max_items]
        self.visible_historic = self.historic_races[:max_items]

        self.dashboard_updated.emit()


class RaceCard(QFrame):
    width = CARD_WIDTH
    height = CARD_HEIGHT

    def __init__(self, race: RaceModel, on_view_race: Callable[[int], None], parent=None):
        super().__init__(parent)

        self.race = race
        self.setFixedSize(self.width, self.height)
        self.setObjectName("card")
        self.setStyleSheet("""
            #card {
                background-color: #333333;
                border-radius: 8px;
            }
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(16, 16, 16, 16)

        name_label = QLabel(race.name)
        name_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        name_label.setWordWrap(True)
        self.layout.addWidget(name_label)

        loc_label = QLabel(race.location)
        loc_label.setStyleSheet("font-size: 14px; font-weight: 500;")
        self.layout.addWidget(loc_label)

        date_label = QLabel(race.date.strftime("%d.%m.%Y"))
        date_label.setStyleSheet("font-size: 13px; color: #AAAAAA;")
        self.layout.addWidget(date_label)

        view_btn = QPushButton("View")
        view_btn.clicked.connect(lambda: on_view_race(self.race.id))
        self.layout.addWidget(view_btn)


class EmptyList(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent)

        self.setFixedHeight(CARD_HEIGHT)

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.layout.setContentsMargins(16, 16, 16, 16)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

        self.layout.addWidget(QLabel(text))


class DashboardFrame(QFrame):
    def __init__(self,
                 content_controller: ContentController,
                 race_service: RaceService,
                 runner_service: RunnerService,
                 event_service: EventService,
                 checkpoint_service: CheckpointService,
                 parent=None):
        super(DashboardFrame, self).__init__(parent)

        self.content_controller = content_controller
        self.race_service = race_service
        self.runner_service = runner_service
        self.event_service = event_service
        self.checkpoint_service = checkpoint_service

        self.model = DashboardViewModel(race_service)
        self.model.dashboard_updated.connect(self.refresh_ui)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(8, 8, 8, 8)
        self.layout.setSpacing(16)

        self.incoming_races_layout = QVBoxLayout()
        self.layout.addLayout(self.incoming_races_layout)
        incoming_label = QLabel("Active Races:")
        incoming_label.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        self.incoming_races_layout.addWidget(incoming_label)

        self.incoming_races_list_layout = QHBoxLayout()
        self.incoming_races_list_layout.setContentsMargins(8, 0, 8, 0)
        self.incoming_races_layout.addLayout(self.incoming_races_list_layout)

        self.historic_races_layout = QVBoxLayout()
        self.layout.addLayout(self.historic_races_layout)
        historic_label = QLabel("Inactive Races:")
        historic_label.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        self.incoming_races_layout.addWidget(historic_label)
        self.historic_races_list_layout = QHBoxLayout()
        self.historic_races_layout.setContentsMargins(8, 0, 8, 0)
        self.historic_races_layout.addLayout(self.historic_races_list_layout)

        self.layout.addStretch()

    def resizeEvent(self, event):
        self.model.update_width(self.width())
        super().resizeEvent(event)

    def refresh_ui(self):
        self.clear_layout(self.incoming_races_list_layout)
        self.clear_layout(self.historic_races_list_layout)

        if len(self.model.visible_incoming) == 0:
            self.incoming_races_list_layout.addWidget(EmptyList("No races incoming"))

        for race in self.model.visible_incoming:
            self.incoming_races_list_layout.addWidget(RaceCard(race, self.view_race))

        if len(self.model.visible_historic) == 0:
            self.historic_races_list_layout.addWidget(EmptyList("No historic races"))

        for race in self.model.visible_historic:
            self.historic_races_list_layout.addWidget(RaceCard(race, self.view_race))

        self.incoming_races_list_layout.addStretch()
        self.historic_races_list_layout.addStretch()

    def clear_layout(self, layout):
        if layout is None:
            return

        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def view_race(self, race_id: int):
        frame = RaceDetailFrame(
            self.race_service,
            self.runner_service,
            self.event_service,
            self.checkpoint_service,
            race_id
        )
        self.content_controller.switch_to_frame(frame)
