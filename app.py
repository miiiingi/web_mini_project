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


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(10000), nullable=False)

    def __repr__(self):
        return f'{self.username} {self.title} 추천 by {self.username}'


with app.app_context():
    db.create_all()
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/newPost')
def newPost():
    return render_template('newPost.html')

if __name__ == '__main__':
    app.run(debug=True)