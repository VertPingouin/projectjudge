from gameobjects.gameobjects import *
import events


class EventManager(events.EventHandler, GameObject):
    """
    An event manager is a EventHandler that handle events by broadcasting them to other event handlers.
    It has no owner and as it has no owner it should be registered within a directory.
    """

    def __init__(self, directory):
        events.EventHandler.__init__(self)
        GameObject.__init__(self, directory, Tags.EVENTMANAGER, Tags.UPDATABLE)

        self.__listeners = {}
        self.__knownhandlers = []
        self._queue = []

        for item in events.EventTypes.__dict__.items():
            if events.EventTypes.validEventName.match(item[0]):
                self.__listeners[item[1]] = []

    def update(self, tick):
        # brodcast events to handlers
        while self._queue:
            self.__handle(self._queue.pop())

        # empty queue
        self._queue = []

    def post(self, event):
        print event
        events.EventHandler.post(self, event)

    def __handle(self, evt):
        # if a handler's owner is in event's argument, we post the event to it
        for handler in self.__knownhandlers:
            if handler.owner in evt.arguments.values():
                handler.post(evt)

        # if a handler subscribed to the event type, we post the event to it
        for listener in self.__listeners[evt.type]:
            listener.post(evt)

    def subscribe(self, handler, eventtype=None):
        # if no eventtype is indicated, we'll send event concerning handler's owner
        if eventtype:
            self.__listeners[eventtype].append(handler)
        else:
            self.__knownhandlers.append(handler)

    def unsubscribe(self, handler, eventtype=None):
        if eventtype:
            try:
                self.__listeners[eventtype].remove(handler)
            except ValueError:
                return False
        else:
            self.__knownhandlers.remove(handler)