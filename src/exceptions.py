
class NotAuthorized(Exception):
    def __str__(self):
        return "Sorry, this user is not authorized to make changes to the Event"


class NotInvited(Exception):
    def __str__(self):
        return "Sorry, this user is not invited to attend the event"


class OverlappingEvents(Exception):
    def __init__(self, event1, event2):
        self.event1 = event1
        self.event2 = event2

    def __str__(self):
        return f"Events {self.event1} and {self.event2} overlap with each other!"


class EventFull(Exception):
    def __str__(self):
        return "Event is already full"


class DuplicateUserException(Exception):
    def __init__(self, user):
        self.user = user

    def __str__(self):
        return f"There has been a duplicate user: {self.user}"
