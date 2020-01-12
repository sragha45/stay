import logging
from datetime import datetime
from typing import List

from .exceptions import NotAuthorized, NotInvited, OverlappingEvents, EventFull
from .model import User, Event

logger = logging.getLogger(__name__)


class EventScheduler:
    def __init__(self, user: User):
        self.user = user

    def create_event(self, event_name: str, start_time: str, end_time: str, is_private: bool = False,
                     invited_users: List[str] = None, attendees_limit: int = 100):

        start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

        event = Event(event_name, start_time, end_time, self.user.email, is_private,
                      invited_users, attendees_limit)

        self.user.created_events.append(event)
        self.user.registered_events.append(event)  # User by default registers himself for the event he created
        event.registered_users.append(self.user.email)

        self.invite_user_for_event(event, self.user)  # User that created the event will be self invited

        return event

    def _is_not_event_creator(self, event: Event):
        return event.event_creator != self.user

    def limit_attendees(self, event: Event, attendees_limit: int):
        if self._is_not_event_creator(event):
            raise NotAuthorized()

        if len(event.registered_users) > attendees_limit:
            raise Exception("Registered users greater than set limit!")

        event.attendees_limit = attendees_limit

    def delete_event(self, event: Event):
        if self._is_not_event_creator(event):
            raise NotAuthorized()

        self.user.registered_events.remove(event)
        self.user.created_events.remove(event)

        del event

    def register_event(self, event: Event):
        if event.is_private:
            if self.user not in event.invited_users:
                raise NotInvited()

        for registered_event in self.user.registered_events:
            if registered_event.overlaps(event):
                raise OverlappingEvents(registered_event, event)

        if len(event.registered_users) == event.attendees_limit:
            raise EventFull()

        self.user.registered_events.append(event)
        event.registered_users.append(self.user)

    def unregister_event(self, event: Event):
        if event in self.user.registered_events:
            self.user.registered_events.remove(event)
            event.registered_users.remove(self.user)

    def invite_user_for_event(self, event: Event, user: User):
        if self._is_not_event_creator(event):
            raise NotAuthorized()

        event.invited_users.append(user.email)


class EventsView:
    def __init__(self, events: List[Event]):
        self.events = events

    def public_events(self):
        return (event for event in self.events if not event.is_private)

    def private_events(self, user: User):
        for event in self.events:
            if event.is_private and user in event.invited_users:
                yield event
