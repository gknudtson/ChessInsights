import redis, os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session

from flask_session import Session
from collections import deque
from dotenv import load_dotenv

from chess_insights.engine.engine import Engine
from chess_insights.game.chess_board import ChessBoard
from chess_insights.util.enum_game_status import GameStatus
from chess_insights.util.enum_square import Square
from chess_insights.util.fen import fen_from_board, board_from_fen
from chess_insights.util.flask_session_JSON_serializer import FlaskSessionJSONSerializer

app = Flask(__name__)

# Configure Flask-Session
load_dotenv()
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000
app.config["SESSION_REDIS"] = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    username=os.getenv("REDIS_USERNAME"),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True,
)

Session(app)
app.session_interface.serializer = FlaskSessionJSONSerializer()


def get_game():
    fen = session.get("fen")
    pgn = session.get("pgn", "")
    board = board_from_fen(fen) if fen else ChessBoard().board_state
    return ChessBoard(board_state=board, pgn=pgn)


def set_game(chess_game):
    session["fen"] = fen_from_board(chess_game.board_state)
    session["pgn"] = chess_game.pgn


def execute_move(from_square,
                 to_square
                 ):
    """Helper function to execute a move and return the response JSON."""
    chess_game = get_game()

    try:
        chess_game.move_piece(from_square, to_square)
        fen = fen_from_board(chess_game.board_state)

        # Check game status after the move
        game_status = chess_game.check_game_status(chess_game.board_state)
        set_game(chess_game)
        history = session.get("history", [])
        history.append((fen_from_board(chess_game.board_state), chess_game.pgn))
        session["history"] = history
        if game_status != GameStatus.ONGOING:
            return {
                'status': 'game_over',
                'game_status': game_status.value,
                'fen': fen,
                'pgn': chess_game.pgn,
            }

        return {'status': 'ok', 'fen': fen, 'pgn': chess_game.pgn}

    except Exception as e:
        return {
            'error': str(e), 'fen': fen_from_board(chess_game.board_state),
            'pgn': chess_game.pgn
        }, 400


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/play', methods=['GET'])
def play():
    """Render the play page with the current board state."""
    return render_template('play.html', fen=session.get("fen"))


@app.route('/game', methods=['GET'])
def game():
    chess_game = get_game()
    fen = fen_from_board(chess_game.board_state)
    pgn = chess_game.pgn
    return render_template('game.html', fen=fen, pgn=pgn)


@app.route('/start_game', methods=['POST'])
def start_game():
    data = request.get_json()
    side = data.get('side', 'white')

    chess_game = ChessBoard()
    if side == 'black':
        engine = Engine(board_state=chess_game.board_state)
        from_square, to_square = engine.generate_move()
        chess_game.move_piece(from_square, to_square)

    set_game(chess_game)
    session["history"] = [(fen_from_board(chess_game.board_state), "")]

    return jsonify({
        "fen": fen_from_board(chess_game.board_state),
        "pgn": chess_game.pgn,
        "color": side,
    })


@app.route('/move', methods=['POST'])
def move():
    """Validate and execute a move."""
    chess_game = get_game()
    data = request.get_json()

    try:
        from_square = Square[data.get('fromSquare')].value
        to_square = Square[data.get('toSquare')].value
        response = execute_move(from_square, to_square)
        return jsonify(response)

    except KeyError as e:
        return jsonify({
            'error': f'Invalid move data: {str(e)}',
            'fen': fen_from_board(chess_game.board_state),
        }), 400
    except ValueError as e:
        return jsonify({
            'error': f'Illegal move attempted: {str(e)}',
            'fen': fen_from_board(chess_game.board_state),
        }), 400
    except Exception as e:
        return jsonify({
            'error': f'Unexpected error: {str(e)}',
            'fen': fen_from_board(chess_game.board_state),
        }), 500


@app.route('/end_game', methods=['POST'])
def end_game():
    """Display appropriate end-game message and reset the game."""
    chess_game = get_game()
    game_status = chess_game.check_game_status(chess_game.board_state)

    if game_status == GameStatus.ONGOING:
        return jsonify({'message': 'Game is still ongoing.',
                        'fen': fen_from_board(chess_game.board_state)}), 400

    # Reset the game
    chess_game = ChessBoard()
    return jsonify({'message': f'Game over: {game_status.value}. New game started.',
                    'fen': fen_from_board(chess_game.board_state)})


@app.route('/engine_move', methods=['GET'])
def engine_move():
    """Get engine move and execute it."""
    chess_game = get_game()
    try:
        engine = Engine(board_state=chess_game.board_state)
        # Get the engine's move
        from_square, to_square = engine.generate_move()
        # Execute the move
        response = execute_move(from_square, to_square)
        return jsonify(response)

    except Exception as e:
        return jsonify({
            'error': f'Unexpected error: {str(e)}',
            'fen': fen_from_board(chess_game.board_state)
        }), 500


@app.route('/set_fen', methods=['POST'])
def set_fen():
    try:
        fen = request.get_json().get('fen')

        # Validate FEN before setting the board
        if not fen or len(fen.split()) != 6:
            return jsonify(
                {'error': 'Invalid FEN format', 'fen': fen}), 400

        chess_game = ChessBoard(fen)
        set_game(chess_game)
        return redirect(url_for('game'))
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}',
                        'fen': fen_from_board(chess_game.board_state)}), 500


@app.route('/undo')
def undo():
    history = session.get("history", [])
    if len(history) <= 1:
        return jsonify({"error": "No moves to undo"}), 400
    history = history[:-2]
    fen, pgn = history[-1]
    chess_game = ChessBoard(fen)
    chess_game.pgn = pgn
    session["history"] = history

    set_game(chess_game)

    return jsonify({"status": "ok", "fen": fen, "pgn": pgn})


if __name__ == '__main__':
    app.run(debug=True)
