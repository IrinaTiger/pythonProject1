from pydantic import BaseModel


class NotificationItem(BaseModel):
    orderId: int
    combinedOrderId: str
    title: str
    date: str
    time: str
    type: str
    unreadMessages: int | None


class NotificationDetails(BaseModel):
    date: str
    time: str
    status: str
    message: str
