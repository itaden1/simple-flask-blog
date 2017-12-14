import sqlite3 as sql
from dbconnect import dbconnect

@dbconnect
def getPosts(cur):
    cur.execute("SELECT * FROM posts WHERE draft = 0")
    posts = cur.fetchall()
    return posts

@dbconnect
def getDrafts(cur):
    cur.execute("SELECT * FROM posts WHERE draft = 1")
    drafts = cur.fetchall()
    return drafts

@dbconnect
def getPostById(cur,postId):
    cur.execute("SELECT * FROM posts WHERE id = (?)",(postId))
    post = cur.fetchall()
    return post

@dbconnect
def getusers(cur):
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    return users

@dbconnect
def updatepass(cur,username,password):
    cur.execute("UPDATE users SET password = ?, username = ? WHERE id = 1",(password,username))

@dbconnect
def getCategories(cur):
    cur.execute("SELECT * FROM tags")
    categories = cur.fetchall()
    return categories

@dbconnect
def getCategoryById(cur,cat_id):
    cur.execute("SELECT * FROM tags WHERE id = ?",cat_id)
    categories = cur.fetchall()
    return categories

@dbconnect
def addcategory(cur,cat):
    cur.execute("INSERT INTO tags (title) VALUES (?)",(cat,))

@dbconnect
def deletecategory(cur,cat):
    cur.execute("DELETE FROM tags WHERE id = ?",cat)
    cur.execute("DELETE FROM post_tag WHERE tag_id = ?",cat)

@dbconnect
def enterpost(cur,title,date,content,author,draft,tags):
    cur.execute("INSERT INTO posts (title, post_date, post, author, draft) VALUES(?,?,?,?,?)",(title,date,content,author,draft))
    posted_id = cur.lastrowid
    for t in tags:
        cur.execute("INSERT INTO post_tag (post_id, tag_id) VALUES(?,?)",(posted_id,t))

@dbconnect
def updatePost(cur,postId,title,date,content,author,draft,tags):
    cur.execute("UPDATE posts SET title = ?, post_date = ?, post = ?, author = ?, draft = ? WHERE id = ? ",(title,date,content,author,draft,postId))
    cur.execute("DELETE FROM post_tag WHERE post_id = ?",postId)
    for t in tags:
        cur.execute("INSERT INTO post_tag (post_id, tag_id) VALUES(?,?)",(postId,t))

@dbconnect
def deletePost(cur,postId):
    cur.execute("DELETE FROM posts WHERE id = ?",(postId))
    cur.execute("DELETE FROM post_tag WHERE post_id = ?",(postId))
    
@dbconnect
def getRelationship(cur):
    cur.execute("SELECT * FROM post_tag")
    rels = cur.fetchall()
    return rels
