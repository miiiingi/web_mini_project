from flask import Flask, render_template
app = Flask(__name__)


# {userId}에 대한 내용이 없어서 그런지 이거 넣으면 오류나서 일단 aoounts로 작성합 
@app.route("/accounts")
def accounts():
    return render_template("mypage.html")


if __name__ == "__main__":
    app.run(debug=True, port=8080)