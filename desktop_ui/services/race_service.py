import json
from dataclasses import dataclass
from datetime import datetime

from PyQt6.QtCore import QObject, pyqtSignal, QUrl
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest


@dataclass
class Race:
    id: int
    name: str
    date: datetime
    location: str
    is_active: bool

    @staticmethod
    def from_dict(data: dict) -> "Race":
        return Race(
            id=data.get("id"),
            name=data.get("name"),
            date=datetime.fromisoformat(data.get("date")),
            location=data.get("location", ""),
            is_active=data.get("is_active", False),
        )


class RaceService(QObject):
    racesLoaded = pyqtSignal(list)
    raceCreated = pyqtSignal(dict)
    errorOccurred = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.manager = QNetworkAccessManager(self)

    def get_races(self):
        request = QNetworkRequest(
            QUrl("http://127.0.0.1:8000/api/races")
        )
        reply = self.manager.get(request)
        reply.finished.connect(
            lambda r=reply: self._on_get_races(r)
        )

    def _on_get_races(self, reply):
        try:
            data = reply.readAll().data()
            races_json = json.loads(data.decode("utf-8"))
            self.racesLoaded.emit([Race.from_dict(r) for r in races_json])
            reply.deleteLater()
        except Exception as e:
            return []


    def create_race(self, payload: dict):
        request = QNetworkRequest(
            QUrl("http://127.0.0.1:8000/api/races")
        )
        request.setHeader(
            QNetworkRequest.KnownHeaders.ContentTypeHeader,
            "application/json",
        )

        reply = self.manager.post(
            request,
            json.dumps(payload).encode("utf-8"),
        )
        reply.finished.connect(
            lambda r=reply: self._on_create_race(r)
        )


    def _on_create_race(self, reply):
        if reply.error():
            self.errorOccurred.emit(reply.errorString())
        else:
            race = json.loads(reply.readAll().data().decode())
            self.raceCreated.emit(race)

        reply.deleteLater()
