import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'userDatabase.db')

userDb = SQLAlchemy(app)

@app.route('/')
def testMain():
    return render_template('test.html')

@app.route('/account/signup/', endpoint='signup')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':  
    app.run(debug=True)