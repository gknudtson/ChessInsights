let board;
let config;
$(document).ready(function () {
    const statusEl = document.getElementById('statusEl');

    config = {
        draggable: true,
        dropOffBoard: 'snapback',
        position: currentFen || "start",
        pieceTheme: '/static/chessboardjs-1.0.0/img/chesspieces/wikipedia/{piece}.png',
        onDrop: function (source, target) {
            handleDrop(source, target);
        }
    };

    board = Chessboard('board', config);

    window.addEventListener("resize", () => {
        board.resize();
    });

// New Game Button Click
    $("#newGameBtn").click(function () {
        board = Chessboard('board', config)
        board.fen(currentFen)
        statusEl.textContent = "New game started!";
    });

    async function handleDrop(source, target) {
        const prev_fen = board.fen();
        if (target === 'offboard' || source === target) return;

        try {
            const response = await fetch('/move', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({fromSquare: source, toSquare: target})
            });

            const data = await response.json();

            if (data.status === 'ok') {
                board.position(data.fen);
                setPGNMoves(data.pgn)
                statusEl.textContent = "Move successful!";
                setTimeout(makeEngineMove, 1);
            } else if (data.status === 'game_over') {
                board.position(data.fen);
                setPGNMoves(data.pgn)
                statusEl.textContent = `Game Over: ${data.game_status}`;
            } else {
                board.position(prev_fen);
                statusEl.textContent = "Move rejected by server.";
            }
        } catch (err) {
            console.error("Error processing move:", err);
            board.position(prev_fen);
            statusEl.textContent = "Server error.";
        }
    }

    async function makeEngineMove() {
        try {
            const response = await fetch('/engine_move', {
                method: 'GET',
                headers: {'Content-Type': 'application/json'}
            });

            const data = await response.json();

            if (data.status === 'ok') {
                board.position(data.fen);
                setPGNMoves(data.pgn)
                statusEl.textContent = "Engine moved.";
            } else if (data.status === 'game_over') {
                board.position(data.fen);
                setPGNMoves(data.pgn)
                statusEl.textContent = `Game Over: ${data.game_status}`;

            } else {
                console.error("Error in engine move:", data);
                statusEl.textContent = "Engine move failed.";
            }
        } catch (err) {
            console.error("Error processing engine move:", err);
            statusEl.textContent = "Server error.";
        }
    }

    function setPGNMoves(pgnString) {
        const pgnContainer = document.querySelector(".pgn-container");
        pgnContainer.innerHTML = "";
        const moves = pgnString.trim().split(/\s+/);

        for (let i = 0; i < moves.length; i += 3) {
            const newRow = document.createElement("div");
            newRow.classList.add("pgn-row");

            // Create move number column
            const moveNumberCol = document.createElement("div");
            moveNumberCol.classList.add("pgn-column");
            moveNumberCol.textContent = `${moves[i]}`;

            // Create button for White's move
            const whiteMoveButton = document.createElement("button");
            whiteMoveButton.classList.add("pgn-button");
            whiteMoveButton.textContent = moves[i + 1]; // White move


            // Create button for Black's move (if exists)
            const blackMoveButton = document.createElement("button");
            blackMoveButton.classList.add("pgn-button");

            if (moves[i + 2]) {
                blackMoveButton.textContent = moves[i + 2]; // Black move
            } else {
                blackMoveButton.textContent = "—"; // Placeholder if no Black move
            }
            // Append elements into the row
            newRow.appendChild(moveNumberCol);
            newRow.appendChild(whiteMoveButton);
            newRow.appendChild(blackMoveButton);

            // Append row into PGN container
            pgnContainer.appendChild(newRow);
        }

        // Auto-scroll to bottom (if necessary)
        pgnContainer.scrollTop = pgnContainer.scrollHeight;
    }

});

async function setFen() {
    try {
        let fenInput = document.getElementById("userInput").value.trim();

        if (!fenInput) {
            alert("Please enter a valid FEN string.");
            return;
        }

        // Send request to the server
        const response = await fetch('/set_fen', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({fen: fenInput})
        });

        const data = await response.json();

        if (response.ok && data.status === "ok") {
            board.position(fenInput);  // Set the board to the new FEN
            document.getElementById("statusEl").textContent = "Board updated to custom FEN.";
        } else {
            alert(`Error: ${data.error || "Invalid FEN entered!"}`);
            console.error("Server error:", data.error);
        }
    } catch (err) {
        console.error("Error setting FEN:", err);
        alert("Failed to update board. Please check your FEN.");
    }
}

document.addEventListener("click", async function (event) {
    if (event.target && event.target.id === "newGameBtn") {
        try {
            const response = await fetch('/new_game', {method: 'GET'});

            if (response.ok) {
                const result = await response.json();
                console.log(result.message);
                currentFen = result.fen;
            } else {
                alert("Failed to start new game.");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("Server error.");
        }
    }
});




