from PyQt6.QtCore import QObject, pyqtSignal, QTimer, QUrl
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest
import json
from dataclasses import dataclass
from typing import Callable

@dataclass
class RunnerModel:
    id: int
    rfid_uid: int
    name: str
    surname: str

    @staticmethod
    def from_dict(data: dict) -> "RunnerModel":
        return RunnerModel(
            id=data.get("id"),
            rfid_uid=data.get("rfid_uid"),
            name=data.get("name"),
            surname=data.get("surname"),
        )


class RunnerService(QObject):
    runnersLoaded = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.manager = QNetworkAccessManager(self)
        self.base_url = "http://127.0.0.1:8000/api/runners"

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.get_runners)
        self.timer.start(1000)  # Poll every 1 second

    def get_runners(self):
        request = QNetworkRequest(QUrl(self.base_url))
        request.setTransferTimeout(10000)
        reply = self.manager.get(request)
        reply.finished.connect(lambda r=reply: self._on_get_runners(r))

    def _on_get_runners(self, reply):
        try:
            data = reply.readAll().data()
            runners_json = json.loads(data.decode("utf-8"))
            self.runnersLoaded.emit([RunnerModel.from_dict(r) for r in runners_json])
        except Exception as e:
            print("Failed to load runners:", e)
        finally:
            reply.deleteLater()

    def delete_runner(self, runner_id: int):
        request = QNetworkRequest(QUrl(f"{self.base_url}/{runner_id}"))
        reply = self.manager.deleteResource(request)
        reply.finished.connect(lambda r=reply: self._on_delete_runner(r))

    def _on_delete_runner(self, reply):
        reply.deleteLater()
        self.get_runners()

    def update_runner_name(self, runner_id: int, new_name: str, new_surname: str = None):
        payload = {"name": new_name}
        if new_surname is not None:
            payload["surname"] = new_surname

        request = QNetworkRequest(QUrl(f"{self.base_url}/{runner_id}"))
        request.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, "application/json")
        reply = self.manager.put(request, json.dumps(payload).encode("utf-8"))
        reply.finished.connect(lambda r=reply: self._on_update_runner(r))

    def _on_update_runner(self, reply):
        reply.deleteLater()
        self.get_runners()


    def get_runners_of_race(self, race_id: int, callback: Callable[[list], None]):
        url = f"http://127.0.0.1:8000/api/runners/?race_id={race_id}"
        request = QNetworkRequest(QUrl(url))
        reply = self.manager.get(request)
        reply.finished.connect(lambda r=reply: self._on_get_runners_of_race(r, callback))

    def _on_get_runners_of_race(self, reply, callback: Callable[[list], None]):
        try:
            data = reply.readAll().data()
            j = json.loads(data.decode("utf-8"))
            items = [RunnerModel.from_dict(x) for x in j]
            callback(items)
        finally:
            reply.deleteLater()

    def create_runner(self, rfid_uid: int, name: str = "", surname: str = ""):
        payload = {"rfid_uid": rfid_uid}
        
        request = QNetworkRequest(QUrl(self.base_url))
        request.setHeader(QNetworkRequest.KnownHeaders.ContentTypeHeader, "application/json")
        
        reply = self.manager.post(request, json.dumps(payload).encode("utf-8"))
        reply.finished.connect(lambda r=reply: self._on_create_runner(r, name, surname))

    def _on_create_runner(self, reply, name: str, surname: str):
        try:
            data = reply.readAll().data()
            response = json.loads(data.decode("utf-8"))
            
            if name or surname:
                runner_id = response.get("id")
                if runner_id:
                    self.update_runner_name(runner_id, name, surname)
            else:
                self.get_runners()
        except Exception as e:
            print("Failed to create runner:", e)
        finally:
            reply.deleteLater()
