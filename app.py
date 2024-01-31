import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

# 회원정보 데이터베이스
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'userDatabase.db')

userDb = SQLAlchemy(app)

class Accounts(userDb.Model):
    id = userDb.Column(userDb.Integer, primary_key=True)
    name = userDb.Column(userDb.String(10), nullable=False)
    email = userDb.Column(userDb.String(100), nullable=False)
    userId = userDb.Column(userDb.String(100), nullable=False)
    password = userDb.Column(userDb.String(100), nullable=False)

    def __repr__(self):
        return f"<Account id={self.id}, name={self.name}, email={self.email}, userId={self.userId}>"
    # 보안 상의 목적으로 패스워드는 리턴 x

with app.app_context():
    userDb.create_all()


# 서버 사이드 관련 코드

@app.route('/')
def testMain():
    return render_template('test.html')

@app.route('/account/signup/', endpoint='signup')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':  
    app.run(debug=True)