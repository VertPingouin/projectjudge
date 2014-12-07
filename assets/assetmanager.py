import re
import os
from spritesheet import SpriteSheet
from asset import Asset


class AssetFolder(dict, Asset):
    def __init__(self):
        Asset.__init__(self)
        dict.__init__({})

    def __getattr__(self, item):
        return self[item]

    def load(self):
        Asset.load(self)
        for item in self.values():
            item.load()

    def unload(self):
        Asset.unload(self)
        for item in self.values():
            item.unload()


class AssetManager(Asset):
    spritesheet = re.compile("spritesheet")

    def __browsefolder(self, folder):
        result = AssetFolder()

        for elt in os.listdir(folder):
            if re.match(AssetManager.spritesheet, elt):
                result[elt.split('.')[0]] = SpriteSheet(os.path.join(folder, elt))
            else:
                result[elt] = self.__browsefolder(os.path.join(folder, elt))

        return result

    def __init__(self, folder):
        Asset.__init__(self)
        self.__root = self.__browsefolder(folder)

    def __getattr__(self, item):
        return self.__root[item]

    def load(self):
        Asset.load(self)
        for item in self.__root.values():
            item.load()

    def unload(self):
        Asset.unload(self)
        for item in self.__root.values():
            item.unload()
