import logging
import unittest
from datetime import datetime

from src.actions import EventScheduler, EventsView
from src.model import User

logger = logging.getLogger(__name__)


class EventsViewTest(unittest.TestCase):
    def setUp(self) -> None:
        self.user = User('sragha45@example.com', 'password')
        self.event_scheduler = EventScheduler(self.user)
        self.event1 = self.event_scheduler.create_event("Event One", '2020-01-12 20:30:00',
                                                        '2020-01-12 22:30:00', is_private=True)
        self.event2 = self.event_scheduler.create_event("Event two", '2020-01-12 22:30:00',
                                                        '2020-01-12 22:30:00', is_private=False)

        self.event3 = self.event_scheduler.create_event("Event three", '2020-01-12 20:30:00',
                                                        '2020-01-12 22:30:00', is_private=True)

        self.list_view = EventsView([self.event1, self.event2, self.event3])

    @staticmethod
    def _create_dummy_user():
        dummy_user = User('dummy', 'dummy')
        dummy_event_scheduler = EventScheduler(dummy_user)

        return dummy_event_scheduler

    def test_view_public_events(self):
        self.assertEqual(len(list(self.list_view.public_events())), 1)

    def test_private_events(self):
        dummy_user = self._create_dummy_user().user
        self.event_scheduler.invite_user_for_event(self.event1, dummy_user)

        self.assertEqual(len(list(self.list_view.private_events(dummy_user))), 1)
