import sqlite3


class Directory:
    def __init__(self):
        self.__con = sqlite3.connect(':memory:')
        self.__cur = self.__con.cursor()

        self.__cur.execute('create table objects '
                           '(id INTEGER PRIMARY KEY, x INTEGER, y INTEGER, z INTEGER)')
        self.__cur.execute('create table tags (id INTEGER PRIMARY KEY, label STRING)')
        self.__cur.execute('create table objects_tags (object_id INTEGER, tag_id INTEGER, flag BOOLEAN)')

        self.__objectidDict = {}

    def __getobjectbyid(self, identifier):
        return self.__objectidDict[identifier]

    # tags operations
    def disabletag(self, obj, tag):
        identifier = id(obj)
        self.__cur.execute(
            'update objects_tags set flag = 0 where tag_id in '
            '(select id from tags where label = "{}") and object_id = {}'.format(tag, identifier)
        )

    def enabletag(self, obj, tag):
        identifier = id(obj)
        self.__cur.execute(
            'update objects_tags set flag = 1 where tag_id in '
            '(select id from tags where label = "{}") and object_id = {}'.format(tag, identifier)
        )

    def register(self, obj, *tags):
        # get id from the object
        identifier = id(obj)
        try:
            posx = obj.position[0]
            posy = obj.position[1]

        except AttributeError:
            posx, posy = 'null', 'null'

        try:
            depth = obj.depth
        except AttributeError:
            depth = 'null'

        # insert the id in object table and store correspondance in dictionnary
        self.__cur.execute('insert into objects values ({}, {}, {}, {})'
                           .format(identifier, posx, posy, depth))
        self.__objectidDict[identifier] = obj

        # insert tags in tags table
        for tag in tags:
            if not self.__cur.execute('select * from tags where label = "{}"'.format(tag)).fetchone():
                self.__cur.execute('insert into tags ("label") values ("{}")'.format(tag))

            tagid = self.__cur.execute('select id from tags where label = "{}"'.format(tag)).fetchone()[0]
            self.__cur.execute('insert into objects_tags values ({}, {}, 1)'.format(identifier, tagid))

    def unregister(self, obj):
        identifier = id(obj)

        # removing ref from correspondances
        self.__objectidDict.pop(identifier)

        # cleaning base, removing object, object tag reference and not used tags
        self.__cur.execute('delete from objects where id = {}'.format(identifier))
        self.__cur.execute('delete from objects_tags where object_id = {}'.format(identifier))
        self.__cur.execute('delete from tags where id not in (select tag_id from objects_tags)')

    def get(self, tag):
        # todo allow to get by update order or draw order, find good way to do it
        self.__cur.execute(
            'select objects.id from objects \
            inner join objects_tags on objects_tags.object_id = objects.id \
            inner join tags on objects_tags.tag_id = tags.id \
            where tags.label = "{}" and flag = 1 order by objects.z'
            .format(tag)
        )

        result = self.__cur.fetchall()

        for i, elt in enumerate(result):
            result[i] = self.__getobjectbyid(result[i][0])

        return result

    def get_single(self, tag):
        self.__cur.execute(
            'select objects.id from objects \
            inner join objects_tags on objects_tags.object_id = objects.id \
            inner join tags on objects_tags.tag_id = tags.id \
            where tags.label = "{}" and flag = 1 order by objects.z'
            .format(tag)
        )
        result = self.__cur.fetchone()
        result = self.__getobjectbyid(result[0])

        return result

    def get_nearest(self, obj, tag):
        posx = obj.position[0]

        self.__cur.execute(
            'select objects.id from objects \
            inner join objects_tags on objects_tags.object_id = objects.id \
            inner join tags on objects_tags.tag_id = tags.id \
            where tags.label = "{}" and flag = 1 a,d x > {} order by objects.x'
            .format(tag, posx)
        )

        try:
            result = self.__cur.fetchone()
            result = self.__getobjectbyid(result[0])
        except TypeError:
            return None

        return result

    def get_tags(self, obj):
        identifier = id(obj)

        self.__cur.execute(
            'select label from tags where id in (select tag_id from objects_tags where object_id = {})'
            .format(identifier)
        )

        result = self.__cur.fetchall()
        for i, elt in enumerate(result):
            result[i] = str(elt[0])

        return result

    def update(self):
        pass


if __name__ == '__main__':
    from extlib.gameobjects.gametime import GameClock

    clock = GameClock()
    clock.start()

    d = Directory()

    class MiniObject():
        def __init__(self, d, position, name, *tags):
            self.position = position
            self.name = name
            self.directory = d
            self.directory.register(self, *tags)

        def __del__(self):
            self.directory.unregister(self)

        def get_nearest(self, tag):
            return self.directory.get_nearest(self, tag)

    cat1 = MiniObject(d, (1, 1), 'Kitty', 'cat')
    dog1 = MiniObject(d, (-1, 1, 0), 'Snoopy', 'dog')
    dog1 = MiniObject(d, (3, 1, 0), 'Medor', 'dog', 'zombie')
    dog1 = MiniObject(d, (4, 1, 0), 'Laika', 'dog', 'zombie')

    time = 0
    for i in range(100):
        prev = clock.get_real_time()
        print d.get('zombie')
        time += (clock.get_real_time() - prev)

    print time
