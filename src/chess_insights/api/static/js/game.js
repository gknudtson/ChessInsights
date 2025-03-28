let fenIndex = localStorage.getItem("fenIndex") ? parseInt(localStorage.getItem("fenIndex")) : 0;
let fenList = localStorage.getItem("fenList") ? JSON.parse(localStorage.getItem("fenList")) : [];
document.addEventListener("DOMContentLoaded", () => {
    playerColor = localStorage.getItem("playerColor") || "white";

    initializeBoard();
    setupEventListeners();
});

/**
 * Initializes the chessboard with configurations and sets the PGN.
 */
function initializeBoard() {
    let isPlay = document.body.classList.contains("play");
    window.board = isPlay ? createStaticBoard() : Chessboard("board", getBoardConfig());
    setPGNMoves(currentPGN);
    // Add initial fen to fenList for pgn buttons on black start.
    if (
        playerColor === "black" &&
        localStorage.getItem("currentFen")?.split(" ").at(-1) === "1"
    ) {
        addFEN(localStorage.getItem("currentFen"));
    }
}

/**
 * Returns the configuration object for Chessboard.js.
 */
function getBoardConfig() {
    return {
        draggable: true,
        dropOffBoard: 'snapback',
        position: localStorage.getItem("currentFen") || "start",
        orientation: playerColor,
        pieceTheme: '/static/chessboardjs-1.0.0/img/chesspieces/wikipedia/{piece}.png',
        onDrop: handleDrop
    };
}

/**
 * Creates a static chessboard where pieces cannot be moved.
 */
function createStaticBoard() {
    const boardConfig = {
        ...getBoardConfig(),
        draggable: false,
    };

    return Chessboard('board', boardConfig);
}

/**
 * Sets up event listeners for various UI interactions.
 */
function setupEventListeners() {
    // Resize event for board responsiveness
    window.addEventListener("resize", () => board.resize());
}

/**
 * Starts a new game by navigating to /play.
 */
function startNewGame() {
    window.location.href = "/play";
}

/**
 * Updates the game state based on server response.
 */
function updateGameState(data, prev_fen = null) {
    if (data.status === 'ok') {
        addFEN(data.fen);
        board.position(data.fen);
        setPGNMoves(data.pgn);
        document.getElementById('statusEl').textContent = "Move successful!";
        localStorage.setItem("currentFen", data.fen);
    } else if (data.status === 'game_over') {
        board = createStaticBoard();
        board.position(data.fen, false);
        setPGNMoves(data.pgn);
        document.getElementById('statusEl').textContent = `Game Over: ${data.game_status}`;
        addFEN(data.fen);
        localStorage.setItem("currentFen", data.fen);
    } else {
        if (prev_fen) board.position(prev_fen);
        document.getElementById('statusEl').textContent = "Move rejected or engine move failed.";
    }
}

/**
 * Handles piece drops, sends move to the server, and updates the board.
 */
async function handleDrop(source, target) {
    if (target === 'offboard' || source === target) return;

    const prev_fen = board.fen();

    try {
        const response = await fetch('/move', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({fromSquare: source, toSquare: target})
        });

        const data = await response.json();
        updateGameState(data, prev_fen);

        if (data.status === 'ok') {
            setTimeout(makeEngineMove, 300);
        }
    } catch (error) {
        console.error("Error processing move:", error);
        board.position(prev_fen);
        document.getElementById('statusEl').textContent = "Server error.";
    }
}

/**
 * Requests an engine move from the server.
 */
async function makeEngineMove() {
    try {
        const response = await fetch('/engine_move', {method: 'GET'});
        const data = await response.json();
        updateGameState(data);
    } catch (error) {
        console.error("Error processing engine move:", error);
        document.getElementById('statusEl').textContent = "Server error.";
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

        // Create move number column
        const moveNumberCol = document.createElement("div");
        moveNumberCol.classList.add("pgn-column");
        moveNumberCol.textContent = moves[i];

        // Create buttons for moves
        const playerMoveButton = createPGNButton(moves[i + 1]);
        const engineMoveButton = createPGNButton(moves[i + 2] || "—");

        // Append elements into the row
        newRow.appendChild(moveNumberCol);
        newRow.appendChild(playerMoveButton);
        newRow.appendChild(engineMoveButton);

        pgnContainer.appendChild(newRow);
    }

    // Auto-scroll to bottom
    pgnContainer.scrollTop = pgnContainer.scrollHeight;
}

/**
 * Creates a PGN move button.
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
        // If current move allow pieces to be moved else can't move in the past board states or mate.
        if (fen === localStorage.getItem("currentFen") && !button.textContent.includes("#")) {
            board = Chessboard('board', getBoardConfig());
        } else {
            board = createStaticBoard();
        }
        board.position(fen, false);
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
    fenList = []
    localStorage.setItem("fenList", fenList);
}

/**
 * Undos most recent player and engine move.
 */
async function undo() {
    try {
        const response = await fetch('/undo', {
            method: 'GET'
        });
        const data = await response.json();
        if (response.ok && data.status === "ok") {
            fenList = fenList.slice(0, -2);
            localStorage.setItem("fenList", JSON.stringify(fenList));
            board = Chessboard('board', getBoardConfig());
            currentFen = data.fen;
            localStorage.setItem("currentFen", currentFen);
            board.position(currentFen);
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
