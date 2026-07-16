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
 * Returns a complete fen string if start is passed or no fen set.
 */
function boardFen(fen) {
    if (!fen || fen === "start") {
        return "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
    }
    return fen;
}

/**
 * Reads whose turn it is from a full FEN string ("w"/"b" field).
 * Falls back to "white" if it can't be determined.
 */
function turnColorFromFen(fen) {
    if (!fen) return "white";
    const parts = fen.split(" ");
    if (parts.length < 2) return "white";
    return parts[1] === "b" ? "black" : "white";
}

/**
 * Base movable config shared between interactive and static boards.
 */
function getMovableConfig() {
    return {
        color: playerColor,
        free: true,
        showDests: true,
        events: {
            after: handleMove
        }
    };
}

/**
 * Initializes the chessground board.
 */
function initializeBoard() {
    const boardElement = document.getElementById("board");
    const config = {
        fen: boardFen(currentFen),
        orientation: playerColor,
        turnColor: turnColorFromFen(currentFen),
        movable: getMovableConfig()
    };
    window.board = Chessground(boardElement, config);
}

/**
 * Locks the board so no pieces can be dragged (used while waiting on the
 * server, and permanently once the game is over).
 */
function disableMovement() {
    window.board.set({ movable: { color: undefined } });
}

/**
 * Re-enables dragging for the player's pieces.
 */
function enableMovement() {
    window.board.set({ movable: { color: playerColor } });
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
    enableMovement();
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
        } else {
            updateGameState(data, prevFen);
        }
    } catch (error) {
        console.error("Error processing move:", error);
        window.board.set({ fen: boardFen(prevFen), turnColor: turnColorFromFen(prevFen) });
        currentFen = prevFen;
        document.getElementById('statusEl').textContent = "Server error.";
        enableMovement();
    }
}

/**
 * Requests an engine move from the server.
 */
async function makeEngineMove() {
    try {
        const response = await fetch('/engine_move', { method: 'GET' });
        const data = await response.json();
        updateGameState(data);
    } catch (error) {
        console.error("Error processing engine move:", error);
        document.getElementById('statusEl').textContent = "Server error.";
        enableMovement();
    }
}

/**
 * Clears the PGN move list.
 */
function clearPGN() {
    const pgnContainer = document.querySelector(".pgn-container");
    if (!pgnContainer) {
        console.error("clearPGN: PGN container not found.");
        return;
    }
    fenIndex = 0;
    localStorage.setItem("fenIndex", fenIndex);
    pgnContainer.innerHTML = "";
}

/**
 * Updates the PGN move list in the UI.
 */
function setPGNMoves(pgnString) {
    clearPGN();

    const pgnContainer = document.querySelector(".pgn-container");
    if (!pgnContainer) {
        console.error("setPGNMoves: PGN container not found.");
        return;
    }

    const moves = pgnString.trim().split(/\s+/);
    if (!moves[0]) return;

    for (let i = 0; i < moves.length; i += 3) {
        const newRow = document.createElement("div");
        newRow.classList.add("pgn-row");

        const moveNumberCol = document.createElement("div");
        moveNumberCol.classList.add("pgn-column");
        moveNumberCol.textContent = moves[i];

        const playerMoveButton = createPGNButton(moves[i + 1]);
        const engineMoveButton = createPGNButton(moves[i + 2] || "—");

        newRow.appendChild(moveNumberCol);
        newRow.appendChild(playerMoveButton);
        newRow.appendChild(engineMoveButton);

        pgnContainer.appendChild(newRow);
    }

    pgnContainer.scrollTop = pgnContainer.scrollHeight;
}

/**
 * Creates a PGN move button. Clicking it shows that historical position;
 * only the live position (current move) remains interactive.
 */
function createPGNButton(text) {
    const button = document.createElement("button");
    button.classList.add("pgn-button");
    button.textContent = text;
    button.fenIndex = fenIndex;

    if (text !== "—") {
        fenIndex++;
    }
    localStorage.setItem("fenIndex", fenIndex);

    button.onclick = function () {
        const fen = button.textContent !== "—" ? getFENs()[this.fenIndex] : getFENs().at(-1);
        const isLiveMove = fen === localStorage.getItem("currentFen") && !button.textContent.includes("#");

        window.board.set({
            fen: boardFen(fen),
            turnColor: turnColorFromFen(fen),
            movable: isLiveMove ? getMovableConfig() : { free: false, color: undefined }
        });
    };

    return button;
}

/**
 * Add given fen to end of fenList.
 */
function addFEN(fen) {
    fenList.push(fen);
    localStorage.setItem("fenList", JSON.stringify(fenList));
}

/**
 * Return local storage fenList as a JS array.
 */
function getFENs() {
    return JSON.parse(localStorage.getItem("fenList")) || [];
}

/**
 * Empty fenList.
 */
function clearFenList() {
    fenList = [];
    localStorage.setItem("fenList", JSON.stringify(fenList));
}

/**
 * Undoes the most recent player and engine move.
 */
async function undo() {
    try {
        const response = await fetch('/undo', { method: 'GET' });
        const data = await response.json();
        if (response.ok && data.status === "ok") {
            fenList = fenList.slice(0, -2);
            localStorage.setItem("fenList", JSON.stringify(fenList));

            currentFen = data.fen;
            localStorage.setItem("currentFen", currentFen);

            window.board.set({
                fen: boardFen(currentFen),
                turnColor: turnColorFromFen(currentFen),
                movable: getMovableConfig()
            });

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