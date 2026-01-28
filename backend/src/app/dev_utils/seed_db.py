import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.crud.race import *
from app.crud.checkpoint import *
from app.crud.event import *
from app.crud.runner import *
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

def nowString():
    return datetime.now().isoformat()

async def seed_db(session: AsyncSession):
    await create_race(
        session,
        RaceCreate(
            name="race1",
            date=datetime.now(),
            is_active=True,
            location = "location1"
    ))

    await create_race(
        session,
        RaceCreate(
            name="race2",
            date=datetime.now(),
            is_active=True,
            location = "location2"
    ))


    await create_race(
        session,
        RaceCreate(
            name="race3",
            date=datetime.now(),
            is_active=False,
            location = "location3"
    ))

    races = (await get_races(session))

    await create_runner(
        session,
        RunnerCreate(
            rfid_uid=1,
        )
    )

    await update_runner(
        session,
        1,
        RunnerUpdate(
            name = "runner1first",
            surname = "runner1sur"
        )
    )

    await create_runner(
        session,
        RunnerCreate(
            rfid_uid=2,
        )
    )

    await update_runner(
        session,
        2,
        RunnerUpdate(
            name = "runner2first",
            surname = "runner2sur"
        )
    )

    await create_runner(
        session,
        RunnerCreate(
            rfid_uid=3,
        )
    )

    await update_runner(
        session,
        3,
        RunnerUpdate(
            name = "runner3first",
            surname = "runner3sur"
        )
    )

    runners = (await get_runners(session))

    await add_race_runner(
        session,
        races[0].id,
        runners[0].id
    )

    await add_race_runner(
        session,
        races[0].id,
        runners[1].id
    )

    await add_race_runner(
        session,
        races[0].id,
        runners[2].id
    )

    await create_checkpoint(
        session,
        CheckpointCreate(
            checkpoint_id="checkpoint1_uuid",
            timestamp=nowString()
        )
    )
    
    await update_checkpoint(
        session,
        1,
        CheckpointUpdate(
            name="checkpoint0name"
        )
    )

    await create_checkpoint(
        session,
        CheckpointCreate(
            checkpoint_id="checkpoint2_uuid",
            timestamp=nowString()
        )
    )

    await update_checkpoint(
        session,
        2,
        CheckpointUpdate(
            name="checkpoint1name"
        )
    )

    await create_checkpoint(
        session,
        CheckpointCreate(
            checkpoint_id="checkpoint3_uuid",
            timestamp=nowString()
        )
    )
    await update_checkpoint(
        session,
        3,
        CheckpointUpdate(
            name="checkpoint2name"
        )
    )

    checkpoints = (await get_checkpoints(session))

    await add_race_checkpoint(
        session,
        races[0].id,
        checkpoints[0].id
    )
    
    await add_race_checkpoint(
        session,
        races[0].id,
        checkpoints[1].id
    )

    await add_race_checkpoint(
        session,
        races[0].id,
        checkpoints[2].id
    )


    await create_event(
        session,
        EventCreate(
            checkpoint_id = checkpoints[0].uuid,
            rfid_uid = 1,
            timestamp = nowString()
        )
    )

    await create_event(
        session,
        EventCreate(
            checkpoint_id = checkpoints[1].uuid,
            rfid_uid = 1,
            timestamp = nowString()
        )
    )

    await create_event(
        session,
        EventCreate(
            checkpoint_id = checkpoints[2].uuid,
            rfid_uid = 1,
            timestamp = nowString()
        )
    )

    await create_event(
            session,
            EventCreate(
                checkpoint_id = checkpoints[0].uuid,
                rfid_uid = 2,
                timestamp = nowString()
            )
        )
