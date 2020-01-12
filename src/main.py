import pprint
from datetime import datetime

from src.db_mapper import EventDBMapper, UserDBMapper
from src.model import User, Event
from src.actions import EventScheduler
from tinydb import TinyDB, Query
from src.repository import UserRepository, EventRepository
import logging

logger = logging.getLogger(__name__)

user_repo = UserRepository()
event_repo = EventRepository()
user = User('sragha45@gmail.com', 'ca$hc0w')
event_scheduler = EventScheduler(user)
event = event_scheduler.create_event("Event One", '2020-01-12 20:30:00',
                                               '2020-01-12 22:30:00', False)





# logger.debug(pprint.pformat(user.to_db_object()))

