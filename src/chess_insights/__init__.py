# # chess_insights/__init__.py
# from flask import Flask
#
# from chess_insights.api.containers.chess_game_container import ChessGameContainer
# from chess_insights.game.chess_board import ChessBoard
# from chess_insights.api.routes.chess_game_routes import chess_game_routes
#
#
# def create_app():
#     game_container = ChessGameContainer()
#     app = Flask(__name__)
#     app.container = game_container
#     app.register_blueprint(chess_game_routes, url_prefix='/game')
#     return app
#
#
# __all__ = ["create_app", "chess_pieces"]
