# chess_insights/__init__.py
from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello_world():  # put application's code here
        return 'Hello World!'

    return app


__all__ = ["chess_pieces"]
