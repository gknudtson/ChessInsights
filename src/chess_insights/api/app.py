from flask import Flask, render_template, request, jsonify, redirect, url_for
from collections import deque

from chess_insights.engine.engine import Engine
from chess_insights.game.chess_board import ChessBoard  # Import your class
from chess_insights.util.enum_game_status import GameStatus
from chess_insights.util.enum_square import Square
from chess_insights.util.fen import fen_from_board

app = Flask(__name__)
chess_game = ChessBoard()
engine = Engine()
board_states = deque(maxlen=10)
board_states.append((chess_game.board_state, chess_game.pgn))


def execute_move(from_square,
                 to_square
                 ):
    """Helper function to execute a move and return the response JSON."""
    global chess_game

    try:
        chess_game.move_piece(from_square, to_square)
        fen = fen_from_board(chess_game.board_state)

        # Check game status after the move
        game_status = chess_game.check_game_status(chess_game.board_state)
        if game_status != GameStatus.ONGOING:
            return {
                'status': 'game_over',
                'game_status': game_status.value,
                'fen': fen,
                'pgn': chess_game.pgn
            }

        return {'status': 'ok', 'fen': fen, 'pgn': chess_game.pgn}

    except Exception as e:
        return {'error': str(e), 'fen': fen_from_board(chess_game.board_state),
                'pgn': chess_game.pgn}, 400


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/play', methods=['GET'])
def play():
    """Render the play page with the current board state."""
    new_game()
    fen = fen_from_board(chess_game.board_state)
    return render_template('play.html', fen=fen)


@app.route('/game', methods=['GET'])
def game():
    fen = fen_from_board(chess_game.board_state)
    pgn = chess_game.pgn
    return render_template('game.html', fen=fen, pgn=pgn)


@app.route('/new_game', methods=['GET'])
def new_game():
    global chess_game, board_states
    chess_game = ChessBoard()
    new_fen = fen_from_board(chess_game.board_state)
    board_states = deque(maxlen=10)
    board_states.append((chess_game.board_state, chess_game.pgn))

    return jsonify({"message": "New game started!", "fen": new_fen})


@app.route('/move', methods=['POST'])
def move():
    """Validate and execute a move."""
    global board_states
    data = request.get_json()

    try:
        from_square = Square[data.get('fromSquare')].value
        to_square = Square[data.get('toSquare')].value
        state_pgn_tuple = (chess_game.board_state.copy(), chess_game.pgn)
        response = execute_move(from_square, to_square)
        return jsonify(response)

    except KeyError as e:
        return jsonify({'error': f'Invalid move data: {str(e)}',
                        'fen': fen_from_board(chess_game.board_state)}), 400
    except ValueError as e:
        return jsonify({'error': f'Illegal move attempted: {str(e)}',
                        'fen': fen_from_board(chess_game.board_state)}), 400
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}',
                        'fen': fen_from_board(chess_game.board_state)}), 500
    finally:
        board_states.append(state_pgn_tuple)


@app.route('/end_game', methods=['POST'])
def end_game():
    """Display appropriate end-game message and reset the game."""
    global chess_game
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
    global engine, chess_game

    try:
        engine = Engine(board_state=chess_game.board_state)
        # Get the engine's move
        from_square, to_square = engine.generate_move()
        # Execute the move
        response = execute_move(from_square, to_square)
        return jsonify(response)

    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}',
                        'fen': fen_from_board(chess_game.board_state)}), 500


@app.route('/set_fen', methods=['POST'])
def set_fen():
    global chess_game
    try:
        fen = request.get_json().get('fen')

        # Validate FEN before setting the board
        if not fen or len(fen.split()) != 6:
            return jsonify(
                {'error': 'Invalid FEN format', 'fen': fen_from_board(chess_game.board_state)}), 400

        chess_game = ChessBoard(fen)
        return redirect(url_for('game'))
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}',
                        'fen': fen_from_board(chess_game.board_state)}), 500


@app.route('/undo', methods=['GET'])
def undo():
    global chess_game, board_states
    if not board_states:
        return jsonify(
            {'error': 'No moves to undo', 'fen': fen_from_board(chess_game.board_state)}), 400
    state = board_states.pop()
    chess_game = ChessBoard(board_state=state[0])
    chess_game.pgn = state[1]
    return jsonify(
        {'status': 'ok', 'fen': fen_from_board(chess_game.board_state), 'pgn': chess_game.pgn})


if __name__ == '__main__':
    app.run(debug=True)
