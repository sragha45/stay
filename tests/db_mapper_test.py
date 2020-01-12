import pprint
import unittest
from src.model import User, Event
from src.actions import EventScheduler
from src.db_mapper import EventDBMapper, UserDBMapper
import logging

logger = logging.getLogger(__name__)

class DBMapperTester(unittest.TestCase):
    def setUp(self) -> None:
        self.user = User('sragha45@example.com', 'password')
        self.event_scheduler = EventScheduler(self.user)
        self.event = self.event_scheduler.create_event("Event One", '2020-01-12 20:30:00',
                                                       '2020-01-12 22:30:00', False)

    def test_to_object_from_dict(self):
        event_db_mapper = EventDBMapper(self.event)
        logger.debug(event_db_mapper.to_db_object())

        # logger.debug(from_db_obj.to_db_object())



