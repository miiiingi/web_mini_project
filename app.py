from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, render_template, request, redirect, url_for
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')
db = SQLAlchemy(app)

class Post_DB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'{self.username} {self.title} 추천 by {self.username}'

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/NewPost', methods = ['GET', 'POST'])
def newPost():
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        # post_db = 
        print(f'title: {title}')
        print(f'content: {content}')
    return render_template('newPost.html')

if __name__ == '__main__':
    app.run(debug=True)