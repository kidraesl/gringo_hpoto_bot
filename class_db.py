import sqlite3
import telebot

bot = telebot.TeleBot(open('config').read())

class Db:
    conn = sqlite3.connect('db_for_test.db', check_same_thread=False)
    cursor = conn.cursor()

    def get_photo(self, id):
        conn = self.conn
        cursor = self.cursor
        next_photo = cursor.execute(f'SELECT * FROM photo WHERE id={id}').fetchone()
        return next_photo[1]

    def insert_photo(self, photo: str, step_photo: int):
        conn = self.conn
        cursor = self.cursor
        cursor.execute('INSERT INTO photo (photo, photo_step) '
                       'VALUES (?, ?)',
                       (photo, step_photo))
        conn.commit()

    def get_photo_step(self, id):
        conn = self.conn
        cursor = self.cursor
        step = cursor.execute(f'SELECT * FROM photo WHERE id={id}').fetchone()
        return step[2]

    def change_photo_dir(self, usid, photo):
        conn = self.conn
        cursor = self.cursor
        cursor.execute(f'UPDATE steps SET photo="{photo}" WHERE user_id = "{usid}"')
        conn.commit()

    def get_photo_dir(self, usid):
        conn = self.conn
        cursor = self.cursor
        photo_dir = cursor.execute(f'SELECT * FROM steps WHERE user_id={usid}').fetchone()
        return photo_dir[7]

    def new_user_to_db(self, user_id: int, user_name: str, user_surname: str,
                         username: str, user_step: int, isadmin: bool):
        conn = self.conn
        cursor = self.cursor
        cursor.execute('INSERT INTO steps (user_id, user_name, user_surname, username, user_step, isadmin) '
                       'VALUES (?, ?, ?, ?, ?, ?)',
                       (user_id, user_name, user_surname, username, user_step, isadmin))
        conn.commit()

    def check_db(self, usid, us_name, us_sname, username, is_admin):
        conn = self.conn
        cursor = self.cursor
        info = cursor.execute('SELECT * FROM steps WHERE user_id=?', (usid,))
        if info.fetchone() is None:
            db = Db()
            db.new_user_to_db(user_id=usid, user_name=us_name, user_surname=us_sname,
                   username=username, user_step=0, isadmin=is_admin)

    def get_id(self, usid):
        conn = self.conn
        cursor = self.cursor
        user = cursor.execute(f'SELECT * FROM steps WHERE user_id ={usid}').fetchone()
        user_id = user[1]
        return user_id

    def get_step(self, usid):
        conn = self.conn
        cursor = self.cursor
        user = cursor.execute(f'SELECT * FROM steps WHERE user_id ={usid}').fetchone()
        user_step = user[5]
        return user_step

    def change_step(self, usid, step):
        conn = self.conn
        cursor = self.cursor
        cursor.execute(f'UPDATE steps SET user_step="{step}" WHERE user_id = "{usid}"')
        conn.commit()


    def get_admin(self, usid):
        conn = self.conn
        cursor = self.cursor
        user = cursor.execute(f'SELECT * FROM steps WHERE user_id ={usid}').fetchone()
        isadmin = user[6]
        return isadmin
