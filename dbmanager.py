#!/usr/bin/python

import MySQLdb

class DbManager():
    def __init__(self, dbHost, dbUser, dbPass, dbName):
        sell.dbCon = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPass, db=dbName, charset='utf8')
        self.dbCursor = self.dbCon.cursor()

    def create_table(self):
        self.drop_table()
        self.dbCursor.execute('CREATE TABLE adb(aid int auto_increment primary key not null, uid varchar(64) not null, state varchar(16) not null, last_update varchar(128) not null)')
        self.dbCon.commit()

    def drop_table(self):
        self.dbCursor.execute('DROP TABLE IF EXISTS adb')
        self.dbCon.commit()

    def create_item(self, uid, state, last_update):
        value = (0, uid, state, last_update)
        self.dbCursor.execute('INSERT INTO adb VALUES(%s,%s,%s,%s)', value)
        self.dbCon.commit()

    def delete_item(self, uid):
        self.dbCursor.execute('DELETE FROM adb WHERE uid=%s', (uid, ))
        self.dbCon.commit()

    def update_state(self, uid, state):
        value = (state, uid)
        self.dbCursor.execute('UPDATE adb SET state=%s WHERE uid=%s', value)
        self.dbCon.commit()

    def get_item(self, uid):
        count = self.dbCursor.execute('SELECT aid, uid, state, last_update FROM adb WHERE uid=%s', (uid,))
        if count:
            item = self.dbCursor.fetchone()
            return item
        return None

    def get_aid(self, uid):
        count = self.dbCursor.execute('SELECT aid FROM adb WHERE uid=%s', (uid,))
        if count:
            aid = self.dbCursor.fetchone()
            return aid[0]
        return None

    def get_state(self, uid):
        count = self.dbCursor.execute('SELECT state FROM adb WHERE uid=%s', (uid,))
        if count:
            state = self.dbCursor.fetchone()
            return state[0]
        return None

    def get_last_update(self, uid):
        count = self.dbCursor.execute('SELECT last_update FROM adb WHERE uid=%s', (uid,))
        if count:
            last_update = self.dbCursor.fetchone()
            return last_update[0]
        return None

    def exists(self, uid):
        if self.get_aid(uid) != None:
            return True
        return False
