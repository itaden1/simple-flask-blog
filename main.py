from flask import Flask, render_template, request, redirect, session, url_for, flash
from passlib.hash import sha256_crypt
from werkzeug.utils import secure_filename
import models as dbhandler
import os, time, requests, json

UPLOAD_FOLDER = './static/uploads/img'
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif'])

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def get_latest_post():
    title = 'Blog'
    posts = dbhandler.getPosts()
    cats = dbhandler.getCategories()
    rels = dbhandler.getRelationship()
    posts = posts[::-1]
    post = posts[:1:]
    tags = []
    tag_gen = ((c for c in cats if c[0] == r[1]) for r in rels if r[0] == post[0][0])
    for tg in tag_gen:
        for t in tg:
            tags.append(t)
    return render_template('post.html', post=post, cats=cats, tags=tags, title=title )

@app.route('/blog-index')
def blog():
    title = 'Blog'
    posts = dbhandler.getPosts()
    cats = dbhandler.getCategories()
    rels = dbhandler.getRelationship()
    posts = posts[::-1]
    return render_template('blog.html', posts=posts, cats=cats, rels=rels, title=title)

@app.route('/posts-by-tag<tagid>')
def get_posts_by_tag(tagid):
    title = 'Blog'
    tagid = tagid
    posts = dbhandler.getPosts()
    rels = dbhandler.getRelationship()
    cats = dbhandler.getCategories()
    search_tag = dbhandler.getCategoryById(tagid)
    searched_posts = ((p for p in posts if p[0] == r[0]) for r in rels if r[1] == int(tagid))
    sp_list = []
    for sp in searched_posts:
        for s in sp:
            sp_list.append(s)
    sp_list = sp_list[::-1]
    return render_template('blog.html', posts=sp_list, cats=cats, search_tag=search_tag, title=title)

@app.route('/view-post<postid>')
def view_post(postid):
    title = 'Blog'
    post = dbhandler.getPostById(postid)
    cats = dbhandler.getCategories()
    rels = dbhandler.getRelationship()
    tags = []
    tag_gen = ((c for c in cats if c[0] == r[1]) for r in rels if r[0] == post[0][0])
    for tg in tag_gen:
        for t in tg:
            tags.append(t)
    return render_template('post.html', post=post, cats=cats, tags=tags, title=title )

@app.route('/new-post')
def new_post():
    if 'username' in session:
        cat_tags = dbhandler.getCategories()
        media = os.listdir('static/uploads/img')
        return render_template('edit-post.html',cat_tags=cat_tags,media=media)
    else:
        return redirect('/blog-latest')

@app.route('/save-post',methods=['POST'])
def save_post():
    if 'username' in session:
        if request.form['submit'] == 'Save Draft':
            draft = 1
        elif request.form['submit'] == 'Publish':
            draft = 0

        tags = request.form.getlist('tag')
        title = request.form['post-title']
        content = request.form['post-content']
        author = request.form['author']
        date = time.strftime("%d/%m/%y")
        dbhandler.enterpost(title,date,content,author,draft,tags)
        return redirect('/posts')
    else:
        return redirect('/blog-latest')

@app.route('/update-post<postId>',methods=['POST'])
def update_post(postId):
    if 'username' in session:
        if request.form['submit'] == 'Save Draft':
            draft = 1
        elif request.form['submit'] == 'Publish':
            draft = 0

        tags = request.form.getlist('tag')
        title = request.form['post-title']
        content = request.form['post-content']
        author = request.form['author']
        date = time.strftime("%d/%m/%y")
        dbhandler.updatePost(postId,title,date,content,author,draft,tags)
        return redirect('/posts')
    else:
        return redirect('/blog-latest')


@app.route('/posts')
def posts():
    if 'username' in session:
        posts = dbhandler.getPosts()
        drafts = dbhandler.getDrafts()
        return render_template('posts.html', posts=posts, drafts=drafts)
    else:
        return redirect('/blog-latest')

@app.route('/edit-post<postId>')
def edit_post(postId):
    if 'username' in session:
        media = os.listdir('static/uploads/img')
        data = dbhandler.getPostById(postId)
        tags = dbhandler.getCategories()
        rels = dbhandler.getRelationship()
        ticked_tags = [r for r in rels if r[0]==data[0][0]]
        return render_template('edit-post.html', data=data, cat_tags=tags, ticked_tags=ticked_tags,media=media)
    else:
        return redirect('/blog-latest')

@app.route('/delete-post<postId>')
def delete_post(postId):
    if 'username' in session:
        dbhandler.deletePost(postId)
        return redirect('/posts')
    else:
        return redirect('/blog-latest')

@app.route('/login', methods=['GET','POST'])
def login():
    if 'username' in session:
        return redirect('/admin')
    if request.method == 'POST':
        error = None

        username = request.form['username']
        password = request.form['password']
        users = dbhandler.getusers();
        hashed_pass = users[0][2]
        if users[0][1] == username:
            match = sha256_crypt.verify(password, hashed_pass)
            if match:
                session['username'] = username
                return redirect(url_for('admin', _external=True))
            else:
                error = 'login failed'
                return render_template('login.html', error=error)
        else:
            error = 'login failed'
            return render_template('login.html', error=error)

    else:
        return render_template('login.html')
         
@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
        return render_template('login.html', message='You were succesfully logged out')
    else:
        return redirect('/blog-latest')

@app.route('/admin')
def admin():
    if 'username' in session:
        cats = dbhandler.getCategories()
        return render_template('settings.html',cats=cats)
    else:
        return redirect('/login')

@app.route('/add-category', methods=['POST'])
def add_category():
    if 'username' in session:
        new_cat = request.form['category']
        dbhandler.addcategory(new_cat)
        return redirect('/admin')
    else:
        return redirect('/blog-latest')

@app.route('/delete-category<catid>')
def delete_category(catid):
    if 'username' in session:
        dbhandler.deletecategory(catid)
        return redirect('/admin')
    else:
        return redirect('/admin')

@app.route('/media')
def manage_media():
    if 'username' in session:
        media = os.listdir('static/uploads/img')
        return render_template('media.html', media=media)
    else:
        redirect('/blog-latest')

@app.route('/upload-media', methods=['POST'])
def upload_media():
    if 'files[]' not in request.files:
        flash('no file part')
        return redirect('/media')
    for ul_file in request.files.getlist('files[]'):
        if ul_file.filename == '':
            flash('no file selected')
        if ul_file and allowed_file(ul_file.filename):
            filename = secure_filename(ul_file.filename)
            ul_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File uploaded succesfully')
        else:
            flash('incorrect filetype')
    return redirect('/media')

def allowed_file(fn):
    return '.' in fn and fn.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/delete-media<filename>')
def delete_media(filename):
    if 'username' in session:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('file deleted')
        return redirect('/media')
    else:
        return redirect('/blog-latest')

@app.route('/manage-db')
def manage_db():
    if 'username' in session:
        posts = dbhandler.getPosts()
        tags = dbhandler.getCategories()
        rels = dbhandler.getRelationship()
        users = dbhandler.getusers()
        return render_template('manage-db.html', posts=posts, tags=tags, rels=rels, users=users)
    else:
        return redirect('/blog-latest')

@app.route('/change-password', methods=['POST'])
def change_password():
    if 'username' in session:
        users = dbhandler.getusers()
        email = request.form['email']
        new_pw = request.form['new-password']
        confirm_pw = request.form['confirm-password']
        if new_pw == confirm_pw:
            hash_pass = sha256_crypt.hash(new_pw)
            dbhandler.updatepass(email,hash_pass)
            flash('Details updated succesfully')
            return redirect(url_for('admin'))
        else:
            flash('Passwords did not match')
            return redirect('/admin')
    else:
        return redirect('/blog-latest')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
