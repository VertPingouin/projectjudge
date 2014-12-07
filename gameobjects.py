# todo implement direction as boolean (right = True, left = False)
import pygame

from locals import Tags
from locals import Parameters
from locals import constants

from extlib.gameobjects.vector2 import Vector2
from extlib.gameobjects.util import lerp


class GameObjectComponent:
    def __init__(self, owner):
        self.owner = owner


class Collider(GameObjectComponent):
    def __init__(self, owner, box):
        GameObjectComponent.__init__(self, owner)
        self.box = box


class RigidBody(GameObjectComponent):
    def __init__(self, owner, mass=1.0, collider=None, lineardrag=1.0, gravityscale=1.0, iskinematic=False):
        GameObjectComponent.__init__(self, owner)
        self. __mass = mass
        self.__lineardrag = lineardrag
        self.__gravityscale = gravityscale
        self.__iskinematic = iskinematic
        self.__resting = False
        self.__physicstate = constants.FALLING
        self.__facing = constants.RIGHT
        self.__cinetic = Vector2(0, 0)
        self.__collider = collider

    @property
    def iskinematic(self):
        return self.__iskinematic

    @property
    def cinetic(self):
        return self.__cinetic

    @property
    def collider(self):
        return self.__collider.box.move(self.owner.position.getposition()[0],
                                        self.owner.position.getposition()[1])

    def update(self, tick):
        # apply gravity
        if not self.__iskinematic and not self.__resting:
            self.__cinetic += Parameters.GRAVITY * self.__gravityscale * tick

            # apply friction
            self.__cinetic.x *= self.__lineardrag

    def push(self, vector):
        self.__cinetic += vector

    def rest(self):
        self.__cinetic = Vector2(self.__cinetic.x, 0)
        self.__resting = True
        self.__physicstate = constants.STANDING


class Position(GameObjectComponent):
    def __init__(self, owner, position=Vector2(0, 0), rigidbody=None):
        GameObjectComponent.__init__(self, owner)

        self.__position = position
        self.__oldposition = position

        self.__rigidbody = rigidbody

    def update(self, tick):
        # compute new position
        self.__oldposition = self.__position.copy()
        self.__position += self.__rigidbody.cinetic * tick

    def getrenderposition(self, betweenframe):
        lp = lerp(Vector2(self.__oldposition[0],
                          self.__oldposition[1]),
                  Vector2(self.__position[0],
                          self.__position[1]),
                  betweenframe)
        return lp

    def getposition(self):
        return self.__position

    def conform(self, other):
        # get a movable close to another instead of going through.
        if self.__rigidbody.collider.top <= other.rigidbody.collider.top <= self.__rigidbody.collider.bottom \
                and not self.__rigidbody.iskinematic:
            self.__position.y = other.rigidbody.collider.top - self.__rigidbody.collider.height

        """
        elif self.owner.physicbody.box.top >= blocker.physicbody.box.bottom >= self.owner.physicbody.box.bottom:
            self.owner.physicbody.box.top = blocker.physicbody.box.bottom

        elif self.owner.physicbody.box.right >= blocker.physicbody.box.right >= self.owner.physicbody.box.left:
            pass

        elif self.owner.physicbody.box.right <= blocker.physicbody.box.left <= self.owner.physicbody.box.left:
            self.owner.physicbody.box.right = blocker.physicbody.box.left
        """


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

        self.collider = Collider(self, pygame.Rect(0, 0, 24, 32))
        self.rigidbody = RigidBody(owner=self, mass=1, collider=self.collider, lineardrag=0.8)
        self.position = Position(owner=self, position=position,rigidbody= self.rigidbody)

    def update(self, tick):
        self.rigidbody.update(tick)
        self.position.update(tick)

    @property
    def frame(self):
        return self.__frame

    @property
    def depth(self):
        return self.__depth


class Blocker(GameObject):
    def __init__(self, d, position, size, depth, *tags):
        GameObject.__init__(self, d, Tags.PHYSIC, *tags)

        self.__depth = depth

        self.collider = Collider(owner=self, box=pygame.Rect((0,0), size))
        self.rigidbody = \
            RigidBody(owner=self, mass=1.0, collider=self.collider, lineardrag=0, gravityscale=1.0, iskinematic=True)
        self.position = Position(owner=self, position=position, rigidbody=self.rigidbody)
