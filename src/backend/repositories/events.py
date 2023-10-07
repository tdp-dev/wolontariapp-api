from beanie.odm.operators.update.general import Set

from backend.models import Event


async def insert_event(**event_data) -> Event:
    return await Event(**event_data).insert()


async def fetch_event(event_id: str) -> Event:
    return await Event.get(event_id)


async def fetch_many_events(page: int = 0, per_page: int = 10) -> list[Event]:
    return await Event.find({}).skip(page * per_page).limit(per_page).to_list()


async def update_event(event: Event, **event_data):
    await event.update(Set(event_data))


async def delete_event(event: Event):
    await event.delete()
