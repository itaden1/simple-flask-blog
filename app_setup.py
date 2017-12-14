import sqlite3 as sql
from sqlite3 import Error
from passlib.hash import sha256_crypt
import sys, os, time

def create_db():
    con = None
    create = False
    db_filename = 'database.db'
    
    print('Checking for existing database file')

    try:
        con = sql.connect(db_filename)
        print('creating database named {}'.format(db_filename))

        print('creating new table "users"')
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS users")
        cur.execute("CREATE TABLE users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL)")
        
        print('creating admin account')
        print('please enter a username:')
        username = input()
        print('please enter a password:')
        password = input()
        sha256_pass = sha256_crypt.hash(password)
        account = (username, sha256_pass)
        cur.execute("INSERT INTO users (username, password) VALUES (?,?)", account)
        

        print('creating table posts')
        now = time.strftime("%d/%m/%y") 
        cur.execute("DROP TABLE IF EXISTS posts")
        cur.execute("CREATE TABLE posts(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, post_date DATE NOT NULL, post TEXT NOT NULL, author TEXT NOT NULL, draft INTEGER NOT NULL)")
        dummy_post = ('Hello Simple Flask Blog', now, '<p>Welcome to Simple Flask Blog!</p><p>You may want to delete this post before you begin</p>', 'Friendly Flask Blogger', 0)
        cur.execute("INSERT INTO posts (title, post_date, post, author, draft) VALUES(?,?,?,?,?)",dummy_post)
        
        print('creating table comments')
        cur.execute("DROP TABLE IF EXISTS comments")
        cur.execute("CREATE TABLE comments(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL, gravitar_url TEXT NOT NULL, comment_date DATE NOT NULL, comment_text TEXT NOT NULL, post_id INTEGER NOT NULL)")
        dummy_comment = ('Commenter', 'commenter@myblog.com', '(.)_(.)', now, 'This is a test comment. Looking great! Please delete this comment',1)
        cur.execute("INSERT INTO comments (name, email, gravitar_url, comment_date, comment_text, post_id) VALUES (?,?,?,?,?,?)",dummy_comment)
        
        print('creating table category tags')
        cur.execute("DROP TABLE IF EXISTS tags")
        cur.execute("CREATE TABLE tags (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL)")
        dummy_tags = [('All',)]
        for t in dummy_tags:
            cur.execute("INSERT INTO tags(title) VALUES (?)",t)

        print('creating tag / post relationship table')
        cur.execute("DROP TABLE IF EXISTS post_tag")
        cur.execute("CREATE TABLE post_tag(post_id INTEGER, tag_id INTEGER)")

        cur.execute("SELECT * FROM posts WHERE id = 1")
        posts = cur.fetchall()
        cur.execute("SELECT * FROM tags")
        tags = cur.fetchall()
        dummy_tag_post_rel = (posts[0][0],tags[0][0])
        cur.execute("INSERT INTO post_tag VALUES (?,?)",dummy_tag_post_rel)

        con.commit()
        
        print('creating secretkey')
        secret_key = os.urandom(24)
        conf_file = 'config.cfg'
        with open(conf_file, 'w') as conf:
            conf.write('SECRET_KEY = {}'.format(secret_key))

    except sql.Error as e:
        if con:
            con.rollback()
        print('ERROR {}'.format(e.args[0]))
        sys.exit(1)

    finally:
        if con:
            con.close()

if __name__ == '__main__':
    create_db()
