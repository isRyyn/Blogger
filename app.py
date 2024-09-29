from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "abc"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='Anonymous')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return 'Blog post ' + str(self.id)

    def header(self):
        return self.content[:200]



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return 'Hello, World!'  

@app.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
    if request.method == 'POST':
        if request.form['user-mail'] == 'raiyyan@mail.com' and request.form['user-pass'] == '1234':
            all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
            return render_template('admin.html', posts=all_posts)
        else:
            flash('Incorrect Email or Password!')
            return render_template('authenticate.html')
    else:
        return render_template('authenticate.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
    return render_template('admin.html', posts=all_posts)


@app.route('/admin/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/admin')


@app.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    
    post = BlogPost.query.get_or_404(id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/admin')
    else:
        return render_template('edit.html', post=post)


@app.route('/posts')
def posts():
    all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
    return render_template('posts.html', posts=all_posts)


@app.route('/admin/new_post', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author'] 
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/admin')
    else:
        return render_template('new_post.html')



@app.route('/posts/blog/<int:id>')
def blog(id):
    post = BlogPost.query.get_or_404(id)
    return render_template('blog.html', post=post)


if __name__ == "__main__":
    app.run(debug=True)