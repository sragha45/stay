from src.model import Event, User
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class DBMapper(ABC):
    @abstractmethod
    def to_db_object(self):
        pass




class UserDBMapper(User, DBMapper):
    def __init__(self, user_obj: User, **kwargs):
        super().__init__(**vars(user_obj), **kwargs)

    def to_db_object(self):
        return dict(email=self.email, password=self.password, authenticated=self.authenticated,
                    created_events=[event.name for event in self.created_events],
                    registered_events=[event.name for event in self.registered_events]
                    )

class EventDBMapper(Event, DBMapper):
    def __init__(self, event_obj: Event, **kwargs):
        super().__init__(**vars(event_obj), **kwargs)

    def to_db_object(self):
        return dict(name=self.name,
                    start_time=self.start_time.timestamp(),
                    end_time=self.end_time.timestamp(),
                    is_private=self.is_private,
                    invited_users=self.invited_users,
                    event_creator=self.event_creator,
                    registered_users=self.registered_users
                    )


class ObjMapper(ABC):
    @abstractmethod
    def to_object_from_dict(self, obj, **kwargs):
        pass


class UserObjMapper(ObjMapper):
    def __init__(self, user_obj, **kwargs):
        super().__init__(**vars(user_obj), **kwargs)

    @staticmethod
    def to_object_from_dict(user_obj: dict, **kwargs):
        user = User(user_obj['email'], user_obj['password'], authenticated=user_obj['authenticated'])
        user.registered_events = kwargs['registered_events']
        user.created_events = kwargs['created_events']

        # logger.debug(user)

        return user


class EventObjMapper(ObjMapper):
    @staticmethod
    def to_object_from_dict(event_obj: dict, **kwargs):
        event = Event(**event_obj)

        return event





