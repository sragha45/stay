import pprint
import unittest
from src.model import User, Event
from src.actions import EventScheduler
from src.repository import UserRepository, EventRepository
import logging

logger = logging.getLogger(__name__)


class RepoTester(unittest.TestCase):
    def setUp(self) -> None:
        self.user = User('sragha45@example.com', 'password')
        self.event_scheduler = EventScheduler(self.user)
        self.user_repo = UserRepository()
        self.event_repo = EventRepository()
        self.event = self.event_scheduler.create_event("Event One", '2020-01-12 20:30:00',
                                                       '2020-01-12 22:30:00', False)

    def test_add_user(self):
        self.user_repo.add_user(user=self.user)

    def test_get_user(self):
        self.user_repo.add_user(user=self.user)
        self.event_repo.add_event(self.event)

        self.assertTrue(self.user_repo.get_user('sragha45@example.com') == self.user)

    def tearDown(self) -> None:
        self.user_repo.delete_repo()
        self.user_repo.close()


