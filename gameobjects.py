import pygame
import events

from locals import Tags
from locals import Parameters
from locals import constants

from extlib.gameobjects.vector2 import Vector2
from extlib.gameobjects.util import lerp


class GameObjectComponent:
    def __init__(self, owner):
        self.owner = owner


class BoxCollider(GameObjectComponent):
    def __init__(self, owner, box):
        GameObjectComponent.__init__(self, owner)
        self.__rectangle = box

    @property
    def rectangle(self):
        return self.__rectangle


class RigidBody(GameObjectComponent):
    def __init__(self, owner, collider=None, lineardrag=1.0, gravityscale=1.0, iskinematic=False):
        GameObjectComponent.__init__(self, owner)

        self.__positioncomponent = owner.position
        self.__lineardrag = lineardrag
        self.__gravityscale = gravityscale
        self.__iskinematic = iskinematic
        self.__resting = False
        self.__physicstate = constants.FALLING
        self.__facing = constants.RIGHT
        self.__cinetic = Vector2(0, 0)
        self.__collider = collider

        self.eventmanager = self.owner._directory.get_single(Tags.EVENTMANAGER)

    @property
    def cinetic(self):
        return self.__cinetic

    @property
    def lineardrag(self):
        return self.__lineardrag

    @property
    def collisionbox(self):
        pos = self.__positioncomponent.getposition()
        return self.__collider.rectangle.move(pos[0], pos[1])

    def update(self, tick):
        if not self.__iskinematic:
            # apply gravity
            self.__cinetic += Parameters.GRAVITY * self.__gravityscale * tick
            self.__cinetic.x *= self.__lineardrag

            self.__positioncomponent.newposition(self.__positioncomponent.getposition() + self.__cinetic * tick)

        else:
            self.__positioncomponent.newposition(self.__positioncomponent.getposition() + self.__cinetic * tick)

        if self.__cinetic.length > Parameters.SPEEDCAP:
            self.__cinetic.length = Parameters.SPEEDCAP

    def push(self, vector):
        self.__resting = False
        self.__cinetic += vector

    def rest(self, on):
        self.__cinetic = Vector2(self.__cinetic.x, 0)
        self.__resting = True
        if self.__physicstate == constants.FALLING:
            self.__physicstate = constants.STANDING
            self.eventmanager.post(events.Event(events.EventTypes.E_PHYSIC_COLLIDE_PHYSIC, gameobjects=(self.owner, on)))

    def conform(self, other):
        # get a movable close to another instead of going through.
        if not self.__iskinematic:
            if self.collisionbox.bottom > other.rigidbody.collisionbox.top > self.collisionbox.top:
                self.__positioncomponent.setverticalposition(other.rigidbody.collisionbox.top
                                                             - self.collisionbox.height)
                self.__lineardrag = other.rigidbody.lineardrag
                self.rest(on=other)

            elif self.collisionbox.top < other.rigidbody.collisionbox.bottom < self.collisionbox.bottom:
                self.__positioncomponent.setverticalposition(other.rigidbody.collisionbox.bottom)
                self.cinetic.y = 0

            elif self.collisionbox.right > other.rigidbody.collisionbox.left and self.cinetic.x > 0:
                self.__positioncomponent.sethorizontalposition(other.rigidbody.collisionbox.left
                                                               - self.collisionbox.width)
                self.cinetic.x = 0

            elif self.collisionbox.left < other.rigidbody.collisionbox.right and self.cinetic.x < 0:
                self.__positioncomponent.sethorizontalposition(other.rigidbody.collisionbox.right)
                self.cinetic.x = 0


class Position(GameObjectComponent):
    def __init__(self, owner, position=Vector2(0, 0)):
        GameObjectComponent.__init__(self, owner)

        self.__position = position
        self.__oldposition = position

    def getrenderposition(self, betweenframe):
        lp = lerp(Vector2(self.__oldposition[0],
                          self.__oldposition[1]),
                  Vector2(self.__position[0],
                          self.__position[1]),
                  betweenframe)
        lp[0] = int(lp[0])
        lp[1] = int(lp[1])
        return lp

    def getposition(self):
        return self.__position

    def newposition(self, position):
        self.__oldposition = self.__position.copy()
        self.__position = position

    def setverticalposition(self, vposition):
        self.__position.y = vposition

    def sethorizontalposition(self, hposition):
        self.__position.x = hposition


class GameObject:
    """
    An object that registers itself in the game directory.
    """

    def __init__(self, d, *tags):
        self._directory = d
        self._directory.register(self, *tags)

    def __repr__(self):
        return "(type: {})".format(self.__class__)

    def __del__(self):
        self._directory.unregister(self)

    # tags operations
    def removetag(self, tag):
        tags = self._directory.get_tags(self)
        tags.remove(tag)
        self._directory.unregister(self)
        self._directory.register(self, *tags)

    def addtag(self, tag):
        tags = self._directory.get_tags(self)
        tags.append(tag)
        self._directory.unregister(self)
        self._directory.register(self, *tags)

    def disabletag(self, tag):
        self._directory.disabletag(self, tag)

    def enabletag(self, tag):
        self._directory.enabletag(self, tag)

    def setdepth(self, depth):
        self._directory.setdepth(self, depth)


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


class Squid(GameObject):
    def __init__(self, d, position, frame, depth, *tags):
        GameObject.__init__(self, d, Tags.VISIBLE, Tags.UPDATABLE, Tags.PHYSIC, *tags)

        self.__frame = frame
        self.__depth = depth

        self.position = Position(
            owner=self,
            position=position,
        )

        self.rigidbody = RigidBody(
            owner=self,
            collider=BoxCollider(owner=self, box=pygame.Rect(0, 0, 24, 32)),
        )

    def update(self, tick):
        self.rigidbody.update(tick)


    @property
    def frame(self):
        return self.__frame

    @property
    def depth(self):
        return self.__depth


class Blocker(GameObject):
    def __init__(self, d, position, size, depth, *tags):
        GameObject.__init__(self, d, Tags.PHYSIC, Tags.BLOCKER, *tags)

        self.__depth = depth

        self.position = Position(
            owner=self,
            position=position,
        )

        self.rigidbody = RigidBody(
            owner=self,
            collider=BoxCollider(owner=self, box=pygame.Rect((0, 0), size)),
            gravityscale=1.0,
            lineardrag=0.95,
            iskinematic=True
        )