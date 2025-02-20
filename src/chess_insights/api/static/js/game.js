document.addEventListener("DOMContentLoaded", () => {
    initializeBoard();
    setupEventListeners();
});

/**
 * Initializes the chessboard with configurations and sets the PGN.
 */
function initializeBoard() {
    window.board = Chessboard('board', getBoardConfig());
    setPGNMoves(currentPGN);
}

/**
 * Returns the configuration object for Chessboard.js.
 */
function getBoardConfig() {
    return {
        draggable: true,
        dropOffBoard: 'snapback',
        position: currentFen || "start",
        pieceTheme: '/static/chessboardjs-1.0.0/img/chesspieces/wikipedia/{piece}.png',
        onDrop: handleDrop
    };
}

/**
 * Sets up event listeners for various UI interactions.
 */
function setupEventListeners() {
    const statusEl = document.getElementById('statusEl');

    // Resize event for board responsiveness
    window.addEventListener("resize", () => board.resize());

    // New game button click event
    document.getElementById("newGameBtn").addEventListener("click", startNewGame);
}

/**
 * Starts a new game by resetting the board and PGN.
 */
function startNewGame() {
    fetch('/new_game', {method: 'GET'})
        .then(response => response.json())
        .then(data => {
            clearPGN();
            board = Chessboard('board', getBoardConfig());
            board.position(data.fen);

            document.getElementById('statusEl').textContent = "New game started!";

        })
        .catch(error => {
            console.error("Error starting new game:", error);
            alert("Server error.");
        });
}

/**
 * Handles piece drops and communicates with the server.
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

        if (data.status === 'ok') {
            board.position(data.fen);
            setPGNMoves(data.pgn);
            document.getElementById('statusEl').textContent = "Move successful!";
            setTimeout(makeEngineMove, 1);
        } else if (data.status === 'game_over') {
            board.position(data.fen);
            setPGNMoves(data.pgn);
            document.getElementById('statusEl').textContent = `Game Over: ${data.game_status}`;
        } else {
            board.position(prev_fen);
            document.getElementById('statusEl').textContent = "Move rejected by server.";
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

        if (data.status === 'ok') {
            board.position(data.fen);
            setPGNMoves(data.pgn);
            document.getElementById('statusEl').textContent = "Engine moved.";
        } else if (data.status === 'game_over') {
            board.position(data.fen);
            setPGNMoves(data.pgn);
            document.getElementById('statusEl').textContent = `Game Over: ${data.game_status}`;
        } else {
            console.error("Error in engine move:", data);
            document.getElementById('statusEl').textContent = "Engine move failed.";
        }
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
        const whiteMoveButton = createPGNButton(moves[i + 1]);
        const blackMoveButton = createPGNButton(moves[i + 2] || "—");

        // Append elements into the row
        newRow.appendChild(moveNumberCol);
        newRow.appendChild(whiteMoveButton);
        newRow.appendChild(blackMoveButton);

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
    return button;
}

/**
 * Sets the board to a user-inputted FEN.
 */
async function setFen() {
    const fenInput = document.getElementById("userInput").value.trim();
    if (!fenInput) {
        alert("Please enter a valid FEN string.");
        return;
    }

    try {
        const response = await fetch('/set_fen', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({fen: fenInput})
        });

        const data = await response.json();

        if (response.ok && data.status === "ok") {
            board.position(fenInput);
            clearPGN()
            document.getElementById("statusEl").textContent = "Board updated to custom FEN.";
        } else {
            alert(`Error: ${data.error || "Invalid FEN entered!"}`);
            console.error("Server error:", data.error);
        }
    } catch (error) {
        console.error("Error setting FEN:", error);
        alert("Failed to update board. Please check your FEN.");
    }
}


// TODO: make pgn buttons set client board to undraggable view of the board at that move
// TODO: Add functionality for undo button


