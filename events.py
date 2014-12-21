"""
This module provides tools to generate, send and handle events of different types
"""

import re
import gameobjects
from locals import Tags
from locals import EngineError


class _EventType:
    """
    Create a new Event Type. Event type consists in an integer code and a dictionnary containing the argument's
    pattern. An event type has two public properties : code and args.
    """
    customEventCounter = 1000

    def __init__(self, code=None, **kwargs):
        # if code is None we create a custom event type
        if code is None:
            _EventType.customEventCounter += 1
            code = _EventType.customEventCounter

        self.__code = code
        self.__argumentPattern = kwargs

    def __repr__(self):
        return str(self.__code)

    # read only attributes

    @property
    def args(self):
        return self.__argumentPattern

    @property
    def code(self):
        return self.__code


class EventTypes:
    """
    EventTypes provides an abstract class that contains all EventType created.
    An EventType can be added via the add method.

    An EventType is formed to match this regexp : '^(E_)[A-Z_]*$'
    """

    validEventName = re.compile('^(E_)[A-Z_]*$')

    # defining default engine events types

    # collision events
    E_BODY_COLLIDE_BODY = _EventType(101, gameobjects=(None, None))
    E_BODY_COLLIDE_PHYSIC = _EventType(102, gameobjects=(None, None))
    E_BODY_COLLIDE_WEAPON = _EventType(103, gameobjects=(None, None))
    E_BODY_COLLIDE_WEAKSPOT = _EventType(104, gameobjects=(None, None))
    E_BODY_COLLIDE_SHIELD = _EventType(105, gameobjects=(None, None))
    E_PHYSIC_COLLIDE_PHYSIC = _EventType(106, gameobjects=(None, None))
    E_PHYSIC_COLLIDE_WEAPON = _EventType(107, gameobjects=(None, None))
    E_PHYSIC_COLLIDE_WEAKSPOT = _EventType(108, gameobjects=(None, None))
    E_PHYSIC_COLLIDE_SHIELD = _EventType(109, gameobjects=(None, None))
    E_WEAPON_COLLIDE_WEAPON = _EventType(110, gameobjects=(None, None))
    E_WEAPON_COLLIDE_WEAKSPOT = _EventType(111, gameobjects=(None, None))
    E_WEAPON_COLLIDE_SHIELD = _EventType(112, gameobjects=(None, None))
    E_WEAKSPOT_COLLIDE_WEAKSPOT = _EventType(113, gameobjects=(None, None))
    E_WEAKSPOT_COLLIDE_SHIELD = _EventType(114, gameobjects=(None, None))
    E_SHIELD_COLLIDE_SHIELD = _EventType(115, gameobjects=(None, None))

    # activity events
    E_ACTIVITY_START = _EventType(201, activity=None, gameobject=None)
    E_ACTIVITY_END = _EventType(202, activity=None, gameobject=None)

    # moving events
    E_MOVING_TOWARD = _EventType(301, gameobjectA=None, gameobjectB=None, distance=None, speed=None, localization=None)
    E_MOVING_AWAY = _EventType(302, gameobjectA=None, gameobjectB=None, distance=None,  speed=None, localization=None)

    E_IS_STILL = _EventType(303, gameobjectA=None, gameobjectB=None, distance=None)

    @staticmethod
    def add(name, **kwargs):
        # add a custom event type
        if EventTypes.validEventName.match(name):
            exec('EventTypes.'+name+'=_EventType(**kwargs)')
        else:
            raise EngineError.BadEventNameError

    def __init__(self):
        pass


class Event:
    """
    An event is a strucutre with a certain type and certain datas respecting the type pattern.
    """

    def __init__(self, etype, **kwargs):
        self.__type = etype

        # we get the base dict from event type
        self.__arguments = etype.args.copy()
        t1 = len(self.__arguments)

        # and update with values passed
        self.__arguments.update(kwargs)
        t2 = len(self.__arguments)

        # if a values passed does not fit the event pattern, raise exceptions
        if t1 < t2:
            invalidargs = []
            for key in self.__arguments.keys():
                if key not in etype.args.keys():
                    invalidargs.append(key)
            raise EngineError.ArgumentError(invalidargs)
        else:
            if None in self.__arguments.values():
                raise EngineError.MissingArgumentError

    def __repr__(self):
        return '<event type: '+str(self.type)+', args: '+str(self.arguments)+'>'

    @property
    def type(self):
        return self.__type

    @property
    def arguments(self):
        return self.__arguments


class EventHandler():
    """
    An EventHandler receive events via the post() public method then handle them in his __handle(event) private method.
    """

    def __init__(self):
        self._queue = []

    def post(self, event):
        # add an event in queue
        self._queue.append(event)

    def update(self, tick):
        while self. _queue:
            event = self._queue.pop()
            self.__handle(event)

    def __handle(self, event):
        # the magic happen here ! Please override this method
        pass

    def __repr__(self):
        return '<EventHandler>'