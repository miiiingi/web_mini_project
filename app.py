import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from sqlalchemy import desc
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))
post_db_file_name = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 'post_db.db')
login_db_file_name = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 'database.db')
app = Flask(__name__)
# 회원정보 데이터베이스
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + login_db_file_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# # 게시글 데이터 베이스
# app.config['SQLALCHEMY_BINDS'] = {
#     'secondary': 'sqlite:///' + post_db_file_name
# }
db = SQLAlchemy(app)

# 시크릿 키 추가
app.secret_key = secrets.token_hex(16)

# 로그인 관련 세팅
login_manager = LoginManager()
login_manager.init_app(app)


class Accounts(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    userId = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Account id={self.id}, name={self.name}, email={self.email}, userId={self.userId}>"
    # 보안 상의 목적으로 패스워드는 리턴 x


class Post_DB(db.Model):
    # __bind_key__ = 'secondary'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=False)
    userId = db.Column(db.Text, nullable=False)
    imgUrl = db.Column(db.Text, nullable=False)
    postNumber = db.Column(db.Integer, nullable=False, 
    default=1)


with app.app_context():
    db.create_all()
    # db.create_all(bind_key='secondary')

# 테스트용 메인 페이지 라우팅


@app.route('/')
def home():
    posts = Post_DB.query.all()
    return render_template('index.html', user=current_user, posts=posts)


@app.route('/newPost/<userId>', methods=['GET', 'POST'])
@login_required
def newPost(userId):
    if request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('content')
        address = request.form.get('address')
        userId = request.form.get('userId')
        imgUrl = request.form.get('imgUrl')
        existing_post = Post_DB.query.filter_by(
            userId=userId).order_by(desc(Post_DB.postNumber)).first()
        if existing_post:
            post_db = Post_DB(
                title=title,
                content=content,
                address=address,
                userId=userId,
                imgUrl=imgUrl,
                postNumber=existing_post.postNumber + 1,
            )
        else:
            post_db = Post_DB(
                title=title,
                content=content,
                address=address,
                userId=userId,
                imgUrl=imgUrl
            )
        db.session.add(post_db)
        db.session.commit()
    return render_template('newPost.html', user=current_user,userId=userId)


@app.route('/userPost/<userId>/<postNumber>')
def userPost(userId, postNumber):
    posts = Post_DB.query.filter_by(userId=userId, postNumber=postNumber)
    return render_template('userPost.html', user=current_user, posts=posts, userId=userId, postNumber=postNumber)


@app.route('/userPost/<userId>')
def userPostAll(userId):
    posts = Post_DB.query.filter_by(userId=userId)
    return render_template('userPost.html', user=current_user, posts=posts, userId=userId)

@app.route('/editPost/<userId>/<postNumber>', methods=['GET', 'POST'])
@login_required
def editPost(userId, postNumber):
    post = Post_DB.query.filter_by(
        userId=userId, postNumber=postNumber).first()
    # if not post:
    #     flash('게시물을 찾을 수 없습니다.', 'danger')
    #     return redirect(url_for('userPost', userId=userId, postNumber=postNumber))

    if request.method == 'POST':
        # 수정된 내용을 받아와서 기존 레코드를 업데이트
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.address = request.form.get('address')
        db.session.commit()
        # flash('게시물이 성공적으로 수정되었습니다.', 'success')
        return redirect(url_for('home'))

    return render_template('editPost.html', user=current_user, posts=post, userId=userId, postNumber=postNumber)

@app.route('/deletePost/<userId>/<postNumber>')
@login_required
def deletePost(userId, postNumber):
    post = Post_DB.query.filter_by(userId=userId, postNumber=postNumber).first()
    if post:
        db.session.delete(post)
        db.session.commit()
        flash('게시물이 성공적으로 삭제되었습니다.', 'success')
    else:
        flash('게시물을 찾을 수 없습니다.', 'danger')
    return redirect(url_for('home'))


@app.route('/completePost/<userId>')
def completePost(userId):
    return render_template('completePost.html', user=current_user,userId=userId)


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
            return render_template('signup.html', error="이미 사용 중인 이메일입니다. 다른 이메일을 입력해주세요.")

        if is_userId_exists(userId):
            return render_template('signup.html', error="이미 사용 중인 아이디입니다. 다른 아이디를 입력해주세요.")

        new_account = Accounts(name=name, email=email,
                               userId=userId, password=password)
        db.session.add(new_account)
        db.session.commit()

        return redirect(url_for('home'))  # 가입 성공 시 원래 화면으로

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
    posts = Post_DB.query.all()
    if request.method == 'POST':
        userId = request.form.get('userId')
        password = request.form.get('password')
        user = Accounts.query.filter_by(userId=userId).first()

        if user and user.password == password:
            login_user(user)
            return redirect(url_for('home'))

        error = "잘못된 아이디 또는 비밀번호입니다. 다시 시도해주세요."

    return render_template('login.html', error=error)


@login_manager.user_loader
def load_user(user_id):
    return Accounts.query.get(int(user_id))

# 로그아웃 기능


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Unauthorized 에러 핸들링


@app.errorhandler(401)
def unauthorized(error):
    return redirect(url_for('home', user=current_user))

# ---------------- 은미 --------------------

# 마이 페이지 
@app.route('/accounts/my')
@login_required
def myPage():
    return render_template('mypage.html', user=current_user)

@app.route('/accounts/edit')
@login_required
def editPage():
    return render_template('edit.html', user=current_user)

@app.route('/accounts/<userId>', methods=['POST'])
@login_required
def update_account(userId):
    # 아이디를 가져와서
    desiredUserId = request.form.get('userId')
    desiredPassword = request.form.get('password')
    desiredEmail = request.form.get('email')

    # 이 아이디를 가진 사용자 정보를 찾아오고
    account = Accounts.query.filter_by(userId=userId).first()

    # 폼에 적어둔 정보로 덮어쓰기
    if account:
        account.userId = desiredUserId
        account.password = desiredPassword
        account.email = desiredEmail

    db.session.commit()
    return render_template('mypage.html', user=current_user)



if __name__ == '__main__':  
    app.run(debug=True)
