from locals import Tags

from extlib.gameobjects.gametime import GameClock
from pygame.time import Clock

from locals import Parameters


class CpuSpinner:
    def __init__(self, directory, ttl=False, gameticks=Parameters.GAMETICKS, gamespeed=Parameters.GAMESPEED):
        self.clock = GameClock(gameticks)
        self.clock.set_speed(gamespeed)
        self.clock.start()

        self.limitclock = Clock()

        self._running = True

        self.__ttl = ttl * Parameters.GAMETICKS

        self._directory = directory

        self.__aupdatecounter = 0

    def __gettick(self):
        return self.clock.game_tick

    def __getbetweenframe(self):
        return self.clock.get_between_frame()

    def start(self):
        self.__loop()

    def __loop(self):
        while self._running:
            for i in self.clock.update():
                self.__update()
            self._draw()

    def __update(self):
        if self.__ttl:
            self.__ttl -= 1
            if self.__ttl == 0:
                self._running = False

        # regular update done x times by seconds
        for updatable in self._directory.get(Tags.UPDATABLE):
            updatable.update(self.__gettick())

        self.__aupdatecounter += 1

        if self.__aupdatecounter == Parameters.AGAMETICKS:
            self.__aupdatecounter = 0
            self._aupdate()

    def _aupdate(self):
        # alternative (heavy update) every x updates
        self._directory.update()
        # print self.clock.average_fps

    def _draw(self):
        self._directory.get_single(Tags.RENDERER).draw(self.__getbetweenframe())
        if Parameters.FPSLIMIT:
            self.limitclock.tick(Parameters.FPSLIMIT)
