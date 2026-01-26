import json
from dataclasses import dataclass
from datetime import datetime
from typing import Callable
from PyQt6.QtCore import QObject, pyqtSignal, QUrl, QTimer
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest


@dataclass
class RaceModel:
    id: int
    name: str
    date: datetime
    location: str
    is_active: bool

    @staticmethod
    def from_dict(data: dict) -> "RaceModel":
        return RaceModel(
            id=data.get("id"),
            name=data.get("name"),
            date=datetime.fromisoformat(data.get("date")),
            location=data.get("location", ""),
            is_active=data.get("is_active", False),
        )


class RaceService(QObject):
    racesLoaded = pyqtSignal(list)
    raceCreated = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.manager = QNetworkAccessManager(self)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.get_races)
        self.timer.start(1000)

    def get_races(self):
        request = QNetworkRequest(
            QUrl("http://127.0.0.1:8000/api/races")
        )
        reply = self.manager.get(request)
        reply.finished.connect(
            lambda r=reply: self._on_get_races(r)
        )

    def get_race_by_id(self, race_id: int, callback: Callable[RaceModel,None]):
        request = QNetworkRequest(QUrl(f"http://127.0.0.1:8000/api/races/{race_id}"))
        reply = self.manager.get(request)
        reply.finished.connect(lambda r=reply: self._on_get_race_by_id(r,callback))

    def _on_get_race_by_id(self, reply, callback: Callable[RaceModel, None]):
        try:
            data = reply.readAll().data()
            j = json.loads(data.decode("utf-8"))
            race = RaceModel.from_dict(j)
            callback(race)
        finally:
            reply.deleteLater()


    def _on_get_races(self, reply):
        try:
            data = reply.readAll().data()
            races_json = json.loads(data.decode("utf-8"))
            self.racesLoaded.emit([RaceModel.from_dict(r) for r in races_json])
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
        race = json.loads(reply.readAll().data().decode())
        self.raceCreated.emit(race)
        reply.deleteLater()



    def delete_race(self, race_id: int):
        request = QNetworkRequest(QUrl(f"http://127.0.0.1:8000/api/races/{race_id}"))
        reply = self.manager.deleteResource(request)
        reply.finished.connect(lambda r=reply: self._on_delete_event(r))

    def _on_delete_event(self, reply):
        reply.deleteLater()
        self.get_races()

    def add_runner_to_race(self, race_id: int, runner_id: int, callback=None):
        request = QNetworkRequest(QUrl(f"http://127.0.0.1:8000/api/races/{race_id}/runners/{runner_id}"))
        request.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, "application/json")
        reply = self.manager.post(request, b"")
        reply.finished.connect(lambda r=reply: self._on_add_runner_to_race(r, callback))

    def _on_add_runner_to_race(self, reply, callback):
        try:
            if reply.error() == reply.NetworkError.NoError:
                if callback:
                    callback(True)
            else:
                if callback:
                    callback(False)
        finally:
            reply.deleteLater()

    def remove_runner_from_race(self, race_id: int, runner_id: int, callback=None):
        request = QNetworkRequest(QUrl(f"http://127.0.0.1:8000/api/races/{race_id}/runners/{runner_id}"))
        reply = self.manager.deleteResource(request)
        reply.finished.connect(lambda r=reply: self._on_remove_runner_from_race(r, callback))

    def _on_remove_runner_from_race(self, reply, callback):
        try:
            if reply.error() == reply.NetworkError.NoError:
                if callback:
                    callback(True)
            else:
                if callback:
                    callback(False)
        finally:
            reply.deleteLater()
