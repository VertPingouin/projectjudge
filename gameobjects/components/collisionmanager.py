from gameobjects.gameobjects import *


class CollisionManager(GameObject):
    def __init__(self, d):
        GameObject.__init__(self, d, Tags.COLLISIONMANAGER, Tags.UPDATABLE)

    def update(self, tick):

        squids = self._directory.get('squidleft')
        blockers = self._directory.get(Tags.BLOCKER)

        for o1 in squids:
            for o2 in blockers:
                if o1.rigidbody.collisionbox.colliderect(o2.rigidbody.collisionbox) and o1 != o2:
                    o1.rigidbody.conform(o2)

