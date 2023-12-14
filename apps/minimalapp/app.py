from email_validator import validate_email, EmailNotValidError
from flask import Flask, render_template, url_for, request, redirect, flash
import logging
from flask_debugtoolbar import DebugToolbarExtension
import os

from flask_mail import Mail, Message

# flask 클래스를 인스턴스화 한다.
app = Flask(__name__)
# Debugtoolbar 띄우기
# app.debug = True

app.config["SECRET_KEY"] = "1gjs25loveya"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

# Mail 클래스의 config를 추가
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

# flask-mail 확장을 등록한다
mail = Mail(app)

# DebugToolbarExtension에 애플리케이션을 설정한다
toolbar = DebugToolbarExtension(app)

# logger의 레벨을 DEBUG로 설정
app.logger.setLevel(logging.DEBUG)

app.logger.critical("fatal error")
app.logger.error("error")
app.logger.debug("debug")

with app.test_request_context("/users?updated=true"):
    # true가 출력된다
    print(request.args.get("updated"))


# url과 실행할 함수를 맵핑한다.
# '127.0.0.1:5000:/'
@app.route("/")
def index():
    return "Hello, Flaskbook!"


# @app.route("/hello")
# def hello():
#     return "Hello World!"

# @app.route("/hello",
#            methods=["GET"],
#            endpoint="hello-endpoint")
# def hello():
#     return "Hello, World!"


@app.route("/hello/<name>", methods=["GET", "POST"], endpoint="hello-endpoint")
def hello(name):
    return f"Hello, {name}!"


@app.route("/name/<name>")
def show_name(name):
    return render_template("index.html", name=name)


# @app.route("/light_check/<command>", methods=["GET", "POST"])
# def light_check(command):
#     return render_template("light_check.html", command=command)


@app.route("/contect")
def contact():
    return render_template("contact.html")


@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        # form의 속성을 사용해서 폼의 값을 취득한다
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        # 입력 체크
        is_valid = True

        if not username:
            flash("사용자명은 필수 입력값입니다")
            is_valid = False

        if not email:
            flash("메일 주소는 필수 입력값입니다")
            is_valid = False

        # 이메일이 유효한지 체크
        try:
            # validate_email 함수가 실행되고
            # 메일이 유효하지 않으면 except로 이동한다
            validate_email(email)
        except EmailNotValidError as e:
            flash("메일 주소의 형식으로 입력해주세요")
            flash(str(e))
            is_valid = False

        if not description:
            flash("문의 내용을 입력해주세요")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))

        # 입력받은 값을 파이썬 변수로 받아오기
        print(username)
        print(email)
        print(description)

        # 이메일을 보낸다
        send_email(
            email,
            "문의 감사합니다",
            "contact_mail",
            username=username,
            description=description,
        )

        # contact 엔드포인트로 리다이렉트한다
        return redirect(url_for("contact_complete"))

    return render_template("contact_complete.html")


def send_email(to, subject, template, **kwargs):
    """메일을 송신하는 함수"""
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)


with app.test_request_context():
    # /
    print(url_for("index"))
    print(url_for("hello-endpoint", name="world"))
    print(url_for("hello-endpoint", name=""))
    print(url_for("show_name", name="AK", page="1"))

# # 애플리케이션 컨텍스트를 취득하여 스택에 push
# ctx = app.app_context()
# ctx.push()

# # current_app에 접근할 수 있게 된다
# print(current_app.name)

# # 전역 임시 영역에 값을 설정한다
# g.connection = "connection"
# print(g.connection)
