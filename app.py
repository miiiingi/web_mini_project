from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
file_name = 'post_db.db'
abs_file_name = os.path.join(os.path.abspath(os.path.dirname(__file__)), file_name)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + abs_file_name
db = SQLAlchemy(app)

class Post_DB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'{self.username} {self.title} 추천 by {self.username}'

with app.app_context():
    if os.path.exists(abs_file_name):
        db.drop_all()
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/newPost', methods = ['GET', 'POST'])
def newPost():
    if request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('content')
        post_db = Post_DB(title = title, content = content)
        db.session.add(post_db)
        db.session.commit()
    return render_template('newPost.html')

@app.route('/completePost')
def completePost():
    return render_template('completePost.html')


if __name__ == '__main__':
    app.run(debug=True)