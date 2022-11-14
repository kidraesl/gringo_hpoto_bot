import sqlite3

def insert_photo(photo: str, step_photo: int):
    conn = sqlite3.connect('db_for_test.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO photo (photo, photo_step) '
                   'VALUES (?, ?)',
                   (photo, step_photo))
    conn.commit()
    conn.close()

def change_photo_dir(usid, photo):
    conn = sqlite3.connect('db_for_test.db', check_same_thread=False)
    curs = conn.cursor()
    curs.execute(f'UPDATE steps SET photo="{photo}" WHERE user_id = "{usid}"')
    conn.commit()
    conn.close()

def get_photo_dir(usid):
    conn = sqlite3.connect('db_for_test.db', check_same_thread=False)
    cursor = conn.cursor()
    photo_dir = cursor.execute(f'SELECT * FROM steps WHERE user_id={usid}').fetchone()
    conn.close()
    return photo_dir[7]

def db_val(user_id: int, user_name: str, user_surname: str, username: str, user_step: int, isadmin: bool):
    conn = sqlite3.connect('db_for_test.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO steps (user_id, user_name, user_surname, username, user_step, isadmin) '
                   'VALUES (?, ?, ?, ?, ?, ?)',
                   (user_id, user_name, user_surname, username, user_step, isadmin))
    conn.commit()
    conn.close()


def get_id(usid):
    conn = sqlite3.connect('db_for_test.db', check_same_thread=False)
    curs = conn.cursor()
    user = curs.execute(f'SELECT * FROM steps WHERE user_id ={usid}').fetchone()
    conn.close()
    user_id = user[1]
    return user_id


def get_step(usid):
    conn = sqlite3.connect('db_for_test.db', check_same_thread=False)
    curs = conn.cursor()
    user = curs.execute(f'SELECT * FROM steps WHERE user_id ={usid}').fetchone()
    conn.close()
    user_step = user[5]
    return user_step


def change_step(usid, step):
    conn = sqlite3.connect('db_for_test.db', check_same_thread=False)
    curs = conn.cursor()
    curs.execute(f'UPDATE steps SET user_step="{step}" WHERE user_id = "{usid}"')
    conn.commit()
    conn.close()


def get_admin(usid):
    conn = sqlite3.connect('db_for_test.db', check_same_thread=False)
    curs = conn.cursor()
    user = curs.execute(f'SELECT * FROM steps WHERE user_id ={usid}').fetchone()
    conn.close()
    isadmin = user[6]
    return isadmin


def check_db(usid, us_name, us_sname, username, is_admin):
    conn = sqlite3.connect('db_for_test.db', check_same_thread=False)
    cursor = conn.cursor()
    info = cursor.execute('SELECT * FROM steps WHERE user_id=?', (usid, ))
    if info.fetchone() is None:
        db_val(user_id=usid, user_name=us_name, user_surname=us_sname,
               username=username, user_step=0, isadmin=is_admin)
        conn.close()
