import pygame

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
    def __init__(self, owner, mass=1.0, collider=None, lineardrag=1.0, gravityscale=1.0, iskinematic=False):
        GameObjectComponent.__init__(self, owner)

        self.__positioncomponent = owner.position
        self.__mass = mass
        self.__lineardrag = lineardrag
        self.__gravityscale = gravityscale
        self.__iskinematic = iskinematic
        self.__resting = False
        self.__physicstate = constants.FALLING
        self.__facing = constants.RIGHT
        self.__cinetic = Vector2(0, 0)
        self.__collider = collider

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
        # apply gravity
        self.__cinetic += Parameters.GRAVITY * self.__gravityscale * tick
        self.__cinetic.x *= self.__lineardrag

        self.__positioncomponent._newposition(self.__positioncomponent.getposition() + self.__cinetic * tick)

    def push(self, vector):
        self.__cinetic += vector

    def rest(self):
        self.__cinetic = Vector2(self.__cinetic.x, 0)
        self.__resting = True
        self.__physicstate = constants.STANDING

    def conform(self, other):
        # get a movable close to another instead of going through.
        if self.collisionbox.top <= other.rigidbody.collisionbox.top <= self.collisionbox.bottom \
                and not self.__iskinematic:
            self.owner.position._setverticalposition(other.rigidbody.collisionbox.top - self.collisionbox.height)
            self.__lineardrag = other.rigidbody.lineardrag
            self.rest()

        # todo left right and top  collisions
        # todo make collisions send events


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

    def _newposition(self, position):
        self.__oldposition = self.__position.copy()
        self.__position = position

    def _setverticalposition(self, vposition):
        self.__position.y = vposition

    def _sethorizontalposition(self, hposition):
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
        tags = self._directory._get_tags(self)
        tags.remove(tag)
        self._directory.unregister(self)
        self._directory.register(self, *tags)

    def addtag(self, tag):
        tags = self._directory._get_tags(self)
        tags.append(tag)
        self._directory.unregister(self)
        self._directory.register(self, *tags)

    def disabletag(self, tag):
        self._directory._disabletag(self, tag)

    def enabletag(self, tag):
        self._directory._enabletag(self, tag)

    def setdepth(self, depth):
        self._directory._setdepth(self, depth)


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
            mass=1,
            collider=BoxCollider(owner=self, box=pygame.Rect(0, 0, 5, 22)),
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
            mass=1.0,
            collider=BoxCollider(owner=self, box=pygame.Rect((0, 0), size)),
            gravityscale=1.0,
            lineardrag=0.95,
            iskinematic=True
        )
