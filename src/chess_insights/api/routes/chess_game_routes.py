from dependency_injector.wiring import inject, Provide
from flask import Blueprint, request

from chess_insights.api.containers.chess_game_container import ChessGameContainer

chess_game_routes = Blueprint('game', __name__)


@chess_game_routes.route('/moves', methods=['GET'])
@inject
def moves(
        chess_board=Provide[ChessGameContainer.chess_board]
):
    square = int(request.args.get('square'))
    color = request.args.get('color')
    piece_key = chess_board.get_piece_on_square(color, square)

    return str(chess_board.get_moves(piece_key, color, 2**square))


@chess_game_routes.route('/start', methods=['GET'])
@inject
def start(
        chess_board=Provide[ChessGameContainer.chess_board]
):
    chess_board.setup()
    return str(chess_board.get_piece_locations("all", "piece"))


@chess_game_routes.route('/end', methods=['GET'])
def end():
    pass
