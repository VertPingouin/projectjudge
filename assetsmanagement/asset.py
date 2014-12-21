from locals import EngineError


class Asset:
    """
    This is the base class for all assetsmanagement
    """
    @staticmethod
    def _missingasset(self):
        raise EngineError.MissingAssetError

    def __init__(self):
        self.loaded = False

    def load(self):
        self.loaded = True

    def unload(self):
        self.loaded = False

    def isloaded(self):
        return self.loaded
