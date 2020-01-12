from datetime import datetime
from typing import List
from pprint import pformat


class User:
    def __init__(self, email: str, password: str, **kwargs):

        self.email = email
        self.password = password
        self.authenticated = False
        self.created_events: List[Event] = []
        self.registered_events: List[Event] = []

        self.__dict__.update(**kwargs)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.email == other
        return self.email == other.email

    def __repr__(self):
        return pformat("<User>: " + str(dict(
            username=self.email,
            authenticated=self.authenticated,
        )))


class Event:
    def __init__(self, name: str, start_time: datetime, end_time: datetime,
                 event_creator: str, is_private: bool,
                 invited_users: List[str] = None, attendees_limit: int = 100, **kwargs):

        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.is_private = is_private
        self.invited_users = invited_users or []
        self.event_creator = event_creator
        self.attendees_limit = attendees_limit
        self.registered_users = []

        self.__dict__.update(**kwargs)

    def overlaps(self, other_event):
        sooner_event, later_event = self, other_event
        if sooner_event.start_time > other_event.start_time:
            sooner_event, other_event = other_event, sooner_event

        return sooner_event.end_time >= other_event.start_time

    def __repr__(self):
        return pformat("<Event>: " + str(dict(
            name=self.name,
            is_private=self.is_private,
            attendees_limit=self.attendees_limit
        )))

