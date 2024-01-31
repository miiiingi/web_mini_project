import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

# 로그인 관련 세팅
login_manager = LoginManager()
login_manager.init_app(app)

# 회원정보 데이터베이스
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')

db = SQLAlchemy(app)

class Accounts(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    userId = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Account id={self.id}, name={self.name}, email={self.email}, userId={self.userId}>"
    # 보안 상의 목적으로 패스워드는 리턴 x

with app.app_context():
    db.create_all()


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
        db.session.add(new_account)
        db.session.commit()
        db.session.close()

        return redirect(url_for('testMain')) # 가입 성공 시 원래 화면으로

    return render_template('signup.html')

# 이메일, 아이디 가입 중복 여부 검증 함수
def is_email_exists(email):
    return bool(Accounts.query.filter_by(email=email).first())

def is_userId_exists(userId):
    return bool(Accounts.query.filter_by(userId=userId).first())

# 로그인 페이지
@app.route('/account/login/', methods=['GET', 'POST'], endpoint='login')
def login():
    error = None
    if request.method == 'POST':
        userId = request.form.get('userId')
        password = request.form.get('password')
        user = Accounts.query.filter_by(userId=userId).first()

        if user and user.password == password:
            login_user(user)
            return redirect(url_for('testMain'))

        error = "잘못된 이메일 또는 비밀번호입니다. 다시 시도해주세요."

    return render_template('login.html', error=error)

# 로그아웃 기능
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('testMain'))

if __name__ == '__main__':  
    app.run(debug=True)