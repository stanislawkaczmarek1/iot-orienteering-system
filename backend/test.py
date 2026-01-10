from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.db.models import Base, Checkpoint, Race
from backend.db.race_repository import RaceRepository

if __name__ == '__main__':
    engine = create_engine('sqlite:///db/test.db')
    Base.metadata.create_all(engine)

    with (Session(engine) as session):
        race_repository = RaceRepository(session)
        print(r := race_repository.get_races()[0])
        print("runners: ", r.race_runners)
        print(race_repository.get_race_runners(r))

        # race_repository.add_race(Race(name="test race", date=datetime.now(), is_active=True))
        # race_repository.add_checkpoint(Checkpoint(name="forest"))
        print(c := race_repository.get_checkpoints())
        # race_repository.add_race_checkpoint(r, c[0])

        print(race_repository.get_race_checkpoints(r))

