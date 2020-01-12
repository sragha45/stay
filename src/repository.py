import logging
from abc import ABC
from typing import List

from tinydb import TinyDB, Query

from src.db_mapper import EventDBMapper, UserDBMapper, EventObjMapper, UserObjMapper
from src.model import User, Event

logger = logging.getLogger(__name__)


class AbstractRepository(ABC):
    def __init__(self):
        self.db = TinyDB('./db.json')

    def close(self):
        self.db.close()

    def delete_repo(self):
        self.db.purge_tables()
        self.db.purge()


class UserRepository(AbstractRepository):
    def __init__(self):
        super(UserRepository, self).__init__()
        self.table = self.db.table('User')

    def add_user(self, user: User):
        user = UserDBMapper(user)
        self.table.insert(user.to_db_object())

    def get_user(self, user_email: str) -> User:
        user = self._find_user(user_email)
        return UserObjMapper.to_object_from_dict(user, registered_events=self.get_registered_events(user_email),
                                                 created_events=self.get_created_events(user_email))

    def get_all_users(self):
        users = self.table.all()
        for user in users:
            yield UserObjMapper.to_object_from_dict(user, registered_events=self.get_registered_events(user['email']),
                                                    created_events=self.get_created_events(user['email']))

    def _find_user(self, user_email: str) -> dict:
        UserQuery = Query()
        users = self.table.search(UserQuery.email == user_email)

        assert len(users) == 1
        user = users[0]

        return user

    def get_registered_events(self, user_email: str) -> List[Event]:
        event_repo = EventRepository()
        user = self._find_user(user_email)
        registered_events = []

        for event in user['registered_events']:
            event = event_repo.get_event(event)
            registered_events.append(event)

        return registered_events

    def get_created_events(self, user_email: str) -> List[Event]:
        event_repo = EventRepository()
        user = self._find_user(user_email)
        registered_events = []

        for event in user['created_events']:
            event = event_repo.get_event(event)
            registered_events.append(event)

        return registered_events


class EventRepository(AbstractRepository):
    def __init__(self):
        super(EventRepository, self).__init__()
        self.table = self.db.table('Event')

    def add_event(self, event: Event):
        eventDBMapper = EventDBMapper(event)
        self.table.insert(eventDBMapper.to_db_object())

    def get_event(self, event_name: str) -> Event:
        EventQuery = Query()
        events = self.table.search(EventQuery.name == event_name)
        assert len(events) == 1

        event = events[0]
        return EventObjMapper.to_object_from_dict(event)
