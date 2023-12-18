from pathlib import Path
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from apps.config import config

# SQLAlchemy 를 인스턴스화 한다
db = SQLAlchemy()

csrf = CSRFProtect()

login_manager = LoginManager()

# login_view 속성에 미로그인시 리다이렉트하는 엔드포인트를 지정한다
login_manager.login_view = "auth.signup"

# login_message 속성에 로그인 후 표시할 메세지 설정
login_manager.login_message = ""


# create_app 함수를 작성한다
def create_app(config_key):
    # 플라스크 인스턴스 생성
    app = Flask(__name__)

    # 앱의 config 설정을 한다
    app.config.from_object(config[config_key])
    app.config.from_mapping(
        SECRET_KEY="{{시크릿키}}",
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        # SQL을 콘솔 로그에 출력하는 설정
        SQLALCHEMY_ECHO=True,
        WTF_CSRF_SECTET_KEY="{{시크릿키}}",
    )

    csrf.init_app(app)

    # SQLAlchemy와 앱을 연계한다
    db.init_app(app)

    # Migrate와 앱을 연계
    Migrate(app, db)

    login_manager.init_app(app)

    # crud 패키지로부터 views를 import 한다
    from apps.crud import views as crud_views

    # register_blueprint 를 사용해 views의 crud를 앱에 등록한다
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    from apps.auth import views as auth_views

    app.register_blueprint(auth_views.auth, url_prefix="/auth")

    return app
