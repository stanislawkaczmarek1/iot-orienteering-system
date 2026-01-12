from typing import List, Callable, Sequence

from backend.db.models import Race, Runner, Checkpoint, RaceCheckpoint, RaceRunner, Event

from sqlalchemy import select, delete
from sqlalchemy.orm import Session


class RaceRepository:
    def __init__(self, session: Session):
        self.session = session

    # Race

    def get_races(self) -> List[Race]:
        return list(self.session.scalars(select(Race)).all())

    def add_race(self, race: Race):
        self.session.add(race)
        self.session.commit()

    def delete_race(self, race: Race):
        self.session.delete(race)
        self.session.commit()

    # Runner

    def get_runners(self) -> Sequence[Runner]:
        return list(self.session.scalars(select(Runner)).all())

    def add_runner(self, runner: Runner):
        self.session.add(runner)
        self.session.commit()

    def delete_runner(self, runner: Runner):
        self.session.delete(runner)
        self.session.commit()

    # Checkpoint

    def get_checkpoints(self) -> Sequence[Checkpoint]:
        return self.session.scalars(select(Checkpoint)).all()

    def add_checkpoint(self, checkpoint: Checkpoint):
        self.session.add(checkpoint)
        self.session.commit()

    def delete_checkpoint(self, checkpoint: Checkpoint):
        self.session.delete(checkpoint)
        self.session.commit()

    # Race Checkpoint

    def get_race_checkpoints(self, race: Race) -> Sequence[Checkpoint]:
        return self.session.scalars(
            select(Checkpoint).join(RaceCheckpoint).where(RaceCheckpoint.race_id == race.id)).all()

    def add_race_checkpoint(self, race: Race, checkpoint: Checkpoint):
        self.session.add(RaceCheckpoint(race_id=race.id, checkpoint_id=checkpoint.id))
        self.session.commit()

    def delete_race_checkpoint(self, race: Race, checkpoint: Checkpoint):
        self.session.execute(delete(RaceCheckpoint).where(RaceCheckpoint.race_id == race.id,
                                                          RaceCheckpoint.checkpoint_id == checkpoint.id))

    # Race Runner

    def get_race_runners(self, race: Race) -> Sequence[Runner]:
        return self.session.scalars(select(Runner).join(RaceRunner).where(RaceRunner.race_id == race.id)).all()

    def add_race_runner(self, race: Race, runner: Runner):
        self.session.add(RaceRunner(race_id=race.id, runner_id=runner.id))
        self.session.commit()

    def delete_race_runner(self, race: Race, runner: Runner):
        self.session.execute(delete(RaceRunner).where(RaceRunner.race_id == race.id, RaceRunner.runner_id == runner.id))
        self.session.commit()

    # Event

    def get_race_runner_events(self, race: Race, runner: Runner) -> Sequence[Event]:
        return self.session.scalars(select(Event).where(Event.race_id == race.id, Event.runner_id == runner.id)).all()

    def add_race_runner_events(self, event: Event):
        return self.session.add(event)
