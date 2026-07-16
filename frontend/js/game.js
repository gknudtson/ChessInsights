import { Chessground } from '@lichess-org/chessground';
import '@lichess-org/chessground/assets/chessground.base.css';
import '@lichess-org/chessground/assets/chessground.brown.css';
import '@lichess-org/chessground/assets/chessground.cburnett.css';
import '../css/game.css';

import {
    initializeBoard, disableMovement, enableMovement, boardFen, turnColorFromFen
} from './board.js'
import {
    addFEN, currentFen, fenList, removeLastTwoFENs, setCurrentFEN, setCurrentPGN, setPlayerColor
} from './state.js'
import { clearPGN, setPGNMoves } from './pgn.js';
import { postMove, fetchEngineMove as apiFetchEngineMove, postUndo } from './api.js';


document.addEventListener("DOMContentLoaded", initPage);

function initPage() {
    setPlayerColor(window.playerColor || localStorage.getItem("playerColor") || "white");
    setCurrentFEN(localStorage.getItem("currentFen") || window.currentFen || "start");
    setCurrentPGN(window.currentPGN || "");
    initializeBoard(handleMove, new Map(Object.entries(window.dests)));
    setupEventListeners();
}

/**
 * Sets up event listeners for various UI interactions.
 */
function setupEventListeners() {
    window.addEventListener("resize", () => window.board.redrawAll());
}

/**
 * Starts a new game by navigating to /play.
 */
function startNewGame() {
    window.location.href = "/play";
}

function updateGameState(data, prevFen = null, prevDests = null) {
    switch (data.status) {
        case "ok":
            addFEN(data.fen);
            setCurrentFEN(data.fen);
            window.board.set({ fen: boardFen(data.fen),
                turnColor: turnColorFromFen(data.fen),
                movable: {dests: new Map(Object.entries(data.dests))}
            });
            setPGNMoves(data.pgn);
            document.getElementById('statusEl').textContent = "Move successful!";
            localStorage.setItem("currentFen", data.fen);
            enableMovement();
            return true;

        case "game_over":
            addFEN(data.fen);
            window.board.set({
                fen: boardFen(data.fen),
                turnColor: turnColorFromFen(data.fen),
                movable: {color: undefined }
            });
            setCurrentFEN(data.fen);
            setPGNMoves(data.pgn);
            document.getElementById('statusEl').textContent = `Game Over: ${data.game_status}`;
            localStorage.setItem("currentFen", data.fen);
            return false;

        default:
            if (prevFen) {
                window.board.set({
                    fen: boardFen(prevFen),
                    turnColor: turnColorFromFen(prevFen),
                    movable: {
                        dests: prevDests,
                    },
                });
                setCurrentFEN(prevFen);
            }
            document.getElementById('statusEl').textContent = "Move rejected or engine move failed.";
            enableMovement();
            return false;
    }
}

/**
 * Fires after the user drags a piece on the board. Sends the move to the
 * server and reconciles the board with the authoritative response.
 */
async function handleMove(orig, dest) {
    const prevFen = currentFen;
    const prevDests = window.board.state['movable']['dests']
    disableMovement();

    try {
        const data = await postMove(orig, dest);
        const shouldMakeEngineMove = updateGameState(data, prevFen, prevDests);
        if (shouldMakeEngineMove) {
            setTimeout(makeEngineMove, 300);
        }
    } catch (error) {
        console.error("Error processing move:", error);
        window.board.set({
            fen: boardFen(prevFen),
            turnColor: turnColorFromFen(prevFen),
            moveable: {dests: prevDests}
        });
        setCurrentFEN(prevFen);
        document.getElementById('statusEl').textContent = "Server error.";
        enableMovement();
    }
}

/**
 * Requests an engine move from the server.
 */
async function makeEngineMove() {
    try {
        const data = await apiFetchEngineMove()
        updateGameState(data, currentFen);
    } catch (error) {
        console.error("Error processing engine move:", error);
        document.getElementById('statusEl').textContent = "Server error.";
        enableMovement();
    }
}



/**
 * Undoes the most recent player and engine move.
 */
async function undo() {
    try {
        const data = await postUndo();
        if (data.status === "ok") {
            removeLastTwoFENs()
            localStorage.setItem("fenList", JSON.stringify(fenList));

            setCurrentFEN(data.fen);
            localStorage.setItem("currentFen", currentFen);

            window.board.set({
                fen: boardFen(currentFen),
                turnColor: turnColorFromFen(currentFen),
                movable: {dests: new Map(Object.entries(data.dests))
            }});

            clearPGN();
            setPGNMoves(data.pgn);
            document.getElementById("statusEl").textContent = "Undo Successful.";
        } else {
            alert(data.error || "Something went wrong when UNDOING.");
        }
    } catch (error) {
        console.error("Error UNDOING:", error);
    }
}

// Exposed for inline onclick="" handlers in game.html
window.startNewGame = startNewGame;
window.undo = undo;