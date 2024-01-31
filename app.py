import os
from flask import Flask, render_template, request, redirect, url_for
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

# 테스트용 메인 페이지 라우팅
@app.route('/')
def testMain():
    return render_template('test.html')

# 회원가입 페이지
@app.route('/account/signup/', methods=['GET', 'POST'], endpoint='signup')
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        userId = request.form['userId']
        password = request.form['password']

        # 중복 유효성 검사
        if is_email_exists(email):
            return render_template('signup.html', error = "이미 사용 중인 이메일입니다. 다른 이메일을 입력해주세요.")

        if is_userId_exists(userId):
            return render_template('signup.html', error = "이미 사용 중인 아이디입니다. 다른 아이디를 입력해주세요.")

        new_account = Accounts(name=name, email=email, userId=userId, password=password)
        userDb.session.add(new_account)
        userDb.session.commit()
        userDb.session.close()

        return redirect(url_for('testMain')) # 가입 성공 시 원래 화면으로

    return render_template('signup.html')

# 이메일, 아이디 가입 중복 여부 검증 함수
def is_email_exists(email):
    return bool(Accounts.query.filter_by(email=email).first())

def is_userId_exists(userId):
    return bool(Accounts.query.filter_by(userId=userId).first())

if __name__ == '__main__':  
    app.run(debug=True)