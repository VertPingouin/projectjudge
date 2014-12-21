import cpuspinner
import directory
import gameobjects
import assetsmanagement

from random import randint
from externallibs.gameobjects.vector2 import Vector2


if __name__ == '__main__':
    # first create directory
    d = directory.Directory()

    # create an event dispatcher
    gameobjects.components.EventManager(d)

    # then create a renderer (an object that draw things in a windows and create opengl context)
    renderer = gameobjects.components.Renderer(d)

    # load ressources
    assets = assetsmanagement.AssetManager('ressourcesfiles')
    assets.load()

    # create the cpu spinner
    spinner = cpuspinner.CpuSpinner(d, ttl=5)

    # create gameobjects
    for i in range(50):
        gameobjects.pawns.Squid(d, Vector2(randint(0, 480-32), randint(0, 270-24)),
                                assets.chinesesquid.spritesheet.left[0], 0, 'squidleft')

    for squid in d.get('squidleft'):
        squid.rigidbody.push(Vector2(randint(-100, 100), randint(-100, -100)))


    gameobjects.pawns.FixSquid(d, Vector2(randint(0, 480-32), randint(0, 270-24)),
                                assets.chinesesquid.spritesheet.up[0], 0)

    gameobjects.pawns.Blocker(d, Vector2(0, -32), Vector2(480, 32), 0)
    gameobjects.pawns.Blocker(d, Vector2(100, 100), Vector2(100, 32), 0)
    gameobjects.pawns.Blocker(d, Vector2(200, 200), Vector2(200, 32), 0)
    gameobjects.pawns.Blocker(d, Vector2(0, 270), Vector2(480, 50), 0)

    gameobjects.pawns.Blocker(d, Vector2(-32, 0), Vector2(32, 270), 0)
    gameobjects.pawns.Blocker(d, Vector2(480, 0), Vector2(32, 270), 0)

    # create things that have an action on previously defined gameobjects
    gameobjects.components.CollisionManager(d)

    # start spinning !
    spinner.start()

