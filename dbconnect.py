import sqlite3 as sql
from sqlite3 import Error

def dbconnect(func):
    def wrapper(*args,**kwargs):
        #con = None
        try:
            con = sql.connect('database.db')
            cur = con.cursor()
            return func(cur,*args,**kwargs)
        except sql.Error as e:
            if con:
                con.rollback()
            print('ERROR {}'.format(e.args[0]))
        finally:
            if con:
                con.commit()
                con.close()
    return wrapper

if __name__ == '__main__':
    dbconnect()
