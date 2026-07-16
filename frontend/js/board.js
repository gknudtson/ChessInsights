import { Chessground } from '@lichess-org/chessground'
import { playerColor, currentFen } from './state.js';
/**
 * Returns a complete fen string if start is passed or no fen set.
 */
export function boardFen(fen) {
    if (!fen || fen === "start") {
        return "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
    }
    return fen;
}

/**
 * Reads whose turn it is from a full FEN string ("w"/"b" field).
 * Falls back to "white" if it can't be determined.
 */
export function turnColorFromFen(fen) {
    if (!fen) return "white";
    const parts = fen.split(" ");
    if (parts.length < 2) return "white";
    return parts[1] === "b" ? "black" : "white";
}

/**
 * Base movable config shared between interactive and static boards.
 */
export function getMovableConfig(moveHandler, dests={}) {
    return {
        color: playerColor,
        free: false,
        showDests: true,
        dests: dests,
        events: {
            after: moveHandler
        }
    };
}

/**
 * Initializes the chessground board.
 */
export function initializeBoard(moveHandler, dests) {
    const boardElement = document.getElementById("board");
    const config = {
        fen: boardFen(currentFen),
        orientation: playerColor,
        turnColor: turnColorFromFen(currentFen),
        movable: getMovableConfig(moveHandler, dests)
    };
    window.board = Chessground(boardElement, config);
}

/**
 * Locks the board so no pieces can be dragged (used while waiting on the
 * server, and permanently once the game is over).
 */
export function disableMovement() {
    window.board.set({ movable: { color: undefined } });
}

/**
 * Re-enables dragging for the player's pieces.
 */
export function enableMovement() {
    window.board.set({ movable: { color: playerColor } });
}