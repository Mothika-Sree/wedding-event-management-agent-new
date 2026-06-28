from app.models.event import Event
from app.data.event_store import event_data


class EventService:

    @staticmethod
    def create_event(event: Event):

        event_data.clear()

        event_data.update(
            event.model_dump()
        )

        return {
            "status": "success",
            "event": event_data
        }

    @staticmethod
    def get_event():

        return event_data