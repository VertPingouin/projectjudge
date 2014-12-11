import cpuspinner
import directory
import renderer
import assets
import physicengine
import gameobjects
from random import randint
from extlib.gameobjects.vector2 import Vector2


if __name__ == '__main__':
    # first create directory
    d = directory.Directory()

    # then create a renderer (an object that draw things in a windows and create opengl context)
    renderer = renderer.Renderer(d)

    # load ressources
    assets = assets.assetmanager.AssetManager('files')
    assets.load()

    # create the cpu spinner
    spinner = cpuspinner.CpuSpinner(d, ttl=3)

    # create gameobjects
    for i in range(100):
        gameobjects.Squid(d, Vector2(240, 30), assets.chinesesquid.spritesheet.left[0], 0, 'squidleft')

    for squid in d.get('squidleft'):
        squid.rigidbody.push(Vector2(randint(-300, 300), randint(-600, -300)))

    gameobjects.Blocker(d, Vector2(100, 100), Vector2(100, 20), 0)
    gameobjects.Blocker(d, Vector2(200, 200), Vector2(200, 20), 0)
    gameobjects.Blocker(d, Vector2(0, 270-11), Vector2(480, 20), 0)

    # create things that have an action on gpreviously defined gameobjects
    physicengine.CollisionManager(d)

    # start spinning !
    spinner.start()
