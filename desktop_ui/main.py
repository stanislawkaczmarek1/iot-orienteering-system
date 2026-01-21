import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import datetime

from backend.db.models import Base, Race, Runner, RaceCheckpoint, Checkpoint, Event
from backend.db.race_repository import RaceRepository
from desktop_ui.main_window import MainWindow

def seed(session: Session):
    rep = RaceRepository(session)
    
    rep.add_race(Race(
            name="race0",
            date=datetime.now(),
            is_active=True,
    ))

    race = rep.get_races()[0]

    rep.add_runner(
        Runner(
            rfid_uid="rfid_uid0",
            name="name0",
            surname="surname0"
        )
    )

    rep.add_runner(
        Runner(
            rfid_uid="rfid_uid1",
            name="name1",
            surname="surname1"
        )
    )

    rep.add_runner(
        Runner(
            rfid_uid="rfid_uid2",
            name="name2",
            surname="surname2"
        )
    )

    rep.add_race_runner(
        race,
        rep.get_runners()[0]
    )

    rep.add_race_runner(
        race,
        rep.get_runners()[1]
    )
    rep.add_race_runner(
        race,
        rep.get_runners()[2]
    )

    rep.add_checkpoint(
        Checkpoint(
            name="checkpoint0"
        )
    )
    rep.add_checkpoint(
        Checkpoint(
            name="checkpoint1"
        )
    )
    rep.add_checkpoint(
        Checkpoint(
            name="checkpoint2"
        )
    )

    rep.add_race_checkpoint(
        race,
        next(filter(lambda cp: cp.name == "checkpoint0", rep.get_checkpoints()), None)
    )
    rep.add_race_checkpoint(
        race,
        next(filter(lambda cp: cp.name == "checkpoint1", rep.get_checkpoints()), None)
    )
    rep.add_race_checkpoint(
        race,
        next(filter(lambda cp: cp.name == "checkpoint2", rep.get_checkpoints()), None)
    )

    rep.add_race_runner_events(
        Event(
            runner_id = rep.get_runners()[0].id,
            checkpoint_id = next(filter(lambda cp: cp.name == "checkpoint0", rep.get_checkpoints()), None).id,
            race_id = race.id,
            timestamp = datetime.now()
        )
    )

    rep.add_race_runner_events(
        Event(
            runner_id = rep.get_runners()[2].id,
            checkpoint_id = next(filter(lambda cp: cp.name == "checkpoint0", rep.get_checkpoints()), None).id,
            race_id = race.id,
            timestamp = datetime.now()
        )
    )

    rep.add_race_runner_events(
        Event(
            runner_id = rep.get_runners()[2].id,
            checkpoint_id = next(filter(lambda cp: cp.name == "checkpoint1", rep.get_checkpoints()), None).id,
            race_id = race.id,
            timestamp = datetime.now()
        )
    )

    rep.add_race_runner_events(
        Event(
            runner_id = rep.get_runners()[2].id,
            checkpoint_id = next(filter(lambda cp: cp.name == "checkpoint2", rep.get_checkpoints()), None).id,
            race_id = race.id,
            timestamp = datetime.now()
        )
    )

    rep.add_race(Race(
            name="race1",
            date=datetime.now(),
            is_active=False,
    ))





def main():
    app = QApplication(sys.argv)

    db_path = "backend/db/test.db"
    
    if os.path.exists(db_path):
        os.remove(db_path)
        
    engine = create_engine(f"sqlite:///{db_path}", echo=False)
    Base.metadata.create_all(engine)

    session = Session(engine)
    seed(session)

    window = MainWindow(session)
    window.show()

    exit_code = app.exec()
    
    session.close()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()