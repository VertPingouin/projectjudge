from externallibs.gameobjects.gametime import GameClock
from events import EventHandler

class Activity(EventHandler):
    """This class shouldn't be used as is, child classes should be used instead"""
    animation = None

    def __init__(self, owner):
        EventHandler.__init__(self)

        self.__owner = owner

        # Activity has its own clock
        self.__clock = GameClock()

        self.__cursor = 0
        self.__prevcursor = -1
        self.__advance = 0.0
        self.__ended = False

        self.__clock.start()
        self.__prevtime = self.__clock.get_real_time()
        self.__time = self.__prevtime

        self._animation = None

    def getframe(self):
        if not self.__ended:
            self.__prevtime = self.__time
            self.__time = self.__clock.get_real_time()
            timedelta = self.__time - self.__prevtime + self.__advance

            while timedelta > self._animation.getduration(self.__cursor):
                timedelta -= self._animation.getduration(self.__cursor)
                self.__cursor += 1

                if self.__cursor > self._animation.length - 1:
                    if self._animation.loop:
                        self.__cursor = 0
                    else:
                        self.__cursor -= 1
                        self.__ended = True

            self.__advance = timedelta

            # update target
            # todo return something with cursor value

        else:
            # execute something when activity ends
            self._onend()

    def __handle(self, event):
        pass

    def _onend(self):
        pass

    @property
    def isended(self):
        return self.__ended


if __name__ == '__main__':
    pass