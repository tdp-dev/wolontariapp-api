from backend.models import Notification, User


async def create_notification(**notification_data) -> Notification:
    return await Notification(**notification_data).insert()


async def remove_notification(notification: Notification) -> None:
    await notification.delete()


async def get_all_notifications(user: User) -> list[Notification]:
    return await Notification.find(Notification.user.id == user.id).to_list()


async def remove_all_notification(user: User):
    await Notification.find(Notification.user.id == user.id).delete()


