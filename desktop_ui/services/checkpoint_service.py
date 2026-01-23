import json
from dataclasses import dataclass

from PyQt6.QtCore import QObject, pyqtSignal, QTimer, QUrl
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest


@dataclass
class CheckpointModel:
    id: int
    uuid: str
    name: str

    @staticmethod
    def from_dict(data: dict) -> "CheckpointModel":
        return CheckpointModel(
            id=data.get("id"),
            uuid=data.get("uuid"),
            name=data.get("name"),
        )


class CheckpointService(QObject):
    checkpointsLoaded = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.manager = QNetworkAccessManager(self)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.get_checkpoints)
        self.timer.start(1000)

    def get_checkpoints(self):
        request = QNetworkRequest(
            QUrl("http://127.0.0.1:8000/api/checkpoints")
        )
        request.setTransferTimeout(10000)
        reply = self.manager.get(request)
        reply.finished.connect(
            lambda r=reply: self._on_get_checkpoints(r)
        )

    def _on_get_checkpoints(self, reply):
        try:
            data = reply.readAll().data()
            checkpoints_json = json.loads(data.decode("utf-8"))
            self.checkpointsLoaded.emit([CheckpointModel.from_dict(r) for r in checkpoints_json])
            reply.deleteLater()
        except Exception as e:
            pass
            # print(e)

    def delete_checkpoint(self, checkpoint_id):
        request = QNetworkRequest(
            QUrl("http://127.0.0.1:8000/api/checkpoints/{}".format(checkpoint_id))
        )

        reply = self.manager.deleteResource(request)
        reply.finished.connect(
            lambda r=reply: self._on_get_checkpoints(r)
        )

    def _delete_checkpoint(self, reply):
        reply.deleteLater()
        self.get_checkpoints()

    def update_checkpoint_name(self, checkpoint_id, new_name):
        print("update checkpoint name")
        request = QNetworkRequest(
            QUrl("http://127.0.0.1:8000/api/checkpoints/{}".format(checkpoint_id))
        )
        request.setHeader(
            QNetworkRequest.KnownHeaders.ContentTypeHeader,
            "application/json",
        )

        reply = self.manager.put(
            request,
            json.dumps({"name": new_name}).encode("utf-8"),
        )

        reply.finished.connect(
            lambda r=reply: self._update_checkpoint_name(r)
        )

    def _update_checkpoint_name(self, reply):
        reply.deleteLater()
        self.get_checkpoints()
