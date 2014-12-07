import cpuspinner
import directory
import renderer
import assets
import physicengine
import gameobjects
from random import randint
from locals import Tags

from extlib.gameobjects.vector2 import Vector2

d = directory.Directory()
renderer = renderer.Renderer(d)

assets = assets.assetmanager.AssetManager('files')
assets.chinesesquid.load()

spinner = cpuspinner.CpuSpinner(d, ttl=3)

gameobjects.Blocker(d, Vector2(0, 100), Vector2(480, 20), 0)
squid = gameobjects.Squid(d, Vector2(100, 30), assets.chinesesquid.spritesheet.left[0], 0, 'squidleft')
squid.rigidbody.push(Vector2(500, -500))
physicengine.CollisionManager(d)

spinner.start()
