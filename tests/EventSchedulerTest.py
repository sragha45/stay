import unittest
from datetime import datetime

from src.actions import EventScheduler
from src.exceptions import EventFull, OverlappingEvents
from src.model import User


class EventSchedulerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.user = User('sragha45@example.com', 'password')
        self.event_scheduler = EventScheduler(self.user)
        self.event = self.event_scheduler.create_event("Event One", '2020-01-12 20:30:00',
                                                       '2020-01-12 22:30:00', False)

    def test_create_event(self):
        assert self.user in self.event.registered_users

    @staticmethod
    def _create_dummy_user():
        dummy_user = User('dummy', 'dummy')
        dummy_event_scheduler = EventScheduler(dummy_user)

        return dummy_event_scheduler

    def test_limit_attendees(self):
        self.assertRaises(Exception, self.event_scheduler.limit_attendees, self.event, 0)

        self.event_scheduler.limit_attendees(self.event, 1)
        dummy_event_scheduler = self._create_dummy_user()

        self.assertRaises(EventFull, dummy_event_scheduler.register_event, self.event)

    def test_delete_event(self):
        self.event_scheduler.delete_event(self.event)

        self.assertEqual(len(self.user.registered_events), 0)

    def test_register_event(self):
        # self.event_scheduler.register_event(self.event)
        dummy_event_scheduler = self._create_dummy_user()
        dummy_event_scheduler.register_event(self.event)

        self.assertEqual(len(self.event.registered_users), 2)
        self.assertEqual(len(self.user.registered_events), 1)
        self.assertEqual(len(dummy_event_scheduler.user.registered_events), 1)

    def test_register_event_overlapping(self):
        self.assertRaises(OverlappingEvents, self.event_scheduler.register_event, self.event)

    def test_unregister_event(self):
        self.event_scheduler.unregister_event(self.event)

        self.assertEqual(len(self.event.registered_users), 0)
        self.assertEqual(len(self.user.registered_events), 0)

    def test_invite_user_for_event(self):
        dummy_user = self._create_dummy_user().user
        self.event_scheduler.invite_user_for_event(self.event, dummy_user)

        self.assertEqual(len(self.event.invited_users), 2)
