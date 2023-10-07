from backend.models import Registration, Event, User
from backend.models.registration import RegistrationStatus

from beanie.odm.operators.update.general import Set


async def insert_registration(**registration_data) -> Registration:
    return await Registration(**registration_data).insert()


async def fetch_one_registration(registration_id: int) -> Registration | None:
    return await Registration.get(registration_id, fetch_links=True)


async def fetch_many_registrations(event: Event, page: int = 0, per_page: int = 10) -> list[Registration]:
    return await Registration.find(Registration.event.id == event.id, fetch_links=True).skip(page * per_page).limit(per_page).to_list()


async def update_registration(registration, **registration_data) -> None:
    await registration.update(Set(registration_data))


async def fetch_user_events_count(user: User) -> int:
    return await Registration.find(
        Registration.user.id == user.id,
        Registration.status == RegistrationStatus.VERIFIED
    ).count()