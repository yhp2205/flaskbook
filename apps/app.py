from flask import Flask


# create_app 함수를 작성한다
def create_app():
    # 플라스크 인스턴스 생성
    app = Flask(__name__)

    # crud 패키지로부터 views를 import 한다
    from apps.crud import views as crud_views

    # register_blueprint 를 사용해 views의 crud를 앱에 등록한다
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    return app
