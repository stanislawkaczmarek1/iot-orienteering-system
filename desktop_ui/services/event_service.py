from PyQt6.QtCore import QObject, pyqtSignal, QTimer, QUrl
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from dataclasses import dataclass
import json
from typing import Callable

@dataclass
class EventModel:
    id: int
    runner_id: int
    checkpoint_id: str
    race_id: int
    timestamp: str

    @staticmethod
    def from_dict(data: dict) -> "EventModel":
        return EventModel(
            id=data.get("id"),
            runner_id=data.get("runner_id"),
            checkpoint_id=data.get("checkpoint_id"),
            race_id=data.get("race_id"),
            timestamp=data.get("timestamp"),
        )

class EventService(QObject):
    eventsLoaded = pyqtSignal(list)
    eventLoaded = pyqtSignal(object)  # For single event
    raceRunnerEventsLoaded = pyqtSignal(list)  # Events for a specific runner in a race

    def __init__(self, parent=None):
        super().__init__(parent)
        self.manager = QNetworkAccessManager(self)
        self.base_url = "http://127.0.0.1:8000/api/events"

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.get_events)
        self.timer.start(1000)

    def get_events(self):
        request = QNetworkRequest(QUrl(self.base_url))
        request.setTransferTimeout(10000)
        reply = self.manager.get(request)
        reply.finished.connect(lambda r=reply: self._on_get_events(r))

    def _on_get_events(self, reply):
        try:
            data = reply.readAll().data()
            events_json = json.loads(data.decode("utf-8"))
            self.eventsLoaded.emit([EventModel.from_dict(e) for e in events_json])
        except Exception as e:
            print("Failed to load events:", e)
        finally:
            reply.deleteLater()

    def delete_event(self, event_id: int):
        request = QNetworkRequest(QUrl(f"{self.base_url}/{event_id}"))
        reply = self.manager.deleteResource(request)
        reply.finished.connect(lambda r=reply: self._on_delete_event(r))

    def _on_delete_event(self, reply):
        reply.deleteLater()
        self.get_events()

    def create_event(self, checkpoint_id: str, rfid_uid: int, timestamp: str):
        payload = {
            "checkpoint_id": checkpoint_id,
            "rfid_uid": rfid_uid,
            "timestamp": timestamp,
        }
        request = QNetworkRequest(QUrl(self.base_url))
        request.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, "application/json")
        reply = self.manager.post(request, json.dumps(payload).encode("utf-8"))
        reply.finished.connect(lambda r=reply: self._on_create_event(r))

    def _on_create_event(self, reply):
        reply.deleteLater()
        self.get_events()


    def get_event(self, event_id: int):
        """Fetch a single event by ID."""
        request = QNetworkRequest(QUrl(f"{self.base_url}/{event_id}"))
        reply = self.manager.get(request)
        reply.finished.connect(lambda r=reply: self._on_get_event(r))

    def _on_get_event(self, reply):
        try:
            data = reply.readAll().data()
            event_json = json.loads(data.decode("utf-8"))
            self.eventLoaded.emit(EventModel.from_dict(event_json))
        except Exception as e:
            print("Failed to load event:", e)
        finally:
            reply.deleteLater()

    def get_race_runner_events(self, race_id: int, runner_id: int):
        """Fetch events for a specific runner in a specific race."""
        url = f"{self.base_url}/race/{race_id}/runner/{runner_id}"
        request = QNetworkRequest(QUrl(url))
        reply = self.manager.get(request)
        reply.finished.connect(lambda r=reply: self._on_get_race_runner_events(r))

    def _on_get_race_runner_events(self, reply):
        try:
            data = reply.readAll().data()
            events_json = json.loads(data.decode("utf-8"))
            self.raceRunnerEventsLoaded.emit([EventModel.from_dict(e) for e in events_json])
        except Exception as e:
            print("Failed to load race runner events:", e)
        finally:
            reply.deleteLater()



    def get_events_of_race(self, race_id: int, callback: Callable[[list], None]):
        url = f"http://127.0.0.1:8000/api/events/?race_id={race_id}"
        request = QNetworkRequest(QUrl(url))
        reply = self.manager.get(request)
        reply.finished.connect(lambda r=reply: self._on_get_events_of_race(r, callback))


    def _on_get_events_of_race(self, reply, callback: Callable[[list], None]):
        try:
            data = reply.readAll().data()
            j = json.loads(data.decode("utf-8"))
            items = [EventModel.from_dict(x) for x in j]
            callback(items)
        finally:
            reply.deleteLater()


