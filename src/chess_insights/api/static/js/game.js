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
                statusEl.textContent = "Move successful!";
                setTimeout(makeEngineMove, 1);
            } else if (data.status === 'game_over') {
                board.position(data.fen);
                statusEl.textContent = `Game Over: ${data.game_status}`;
                board = Chessboard('board', {
                    position: data.fen,
                    draggable: false,
                    pieceTheme: '/static/chessboardjs-1.0.0/img/chesspieces/wikipedia/{piece}.png',
                });
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
                statusEl.textContent = "Engine moved.";
            } else if (data.status === 'game_over') {
                board.position(data.fen);
                statusEl.textContent = `Game Over: ${data.game_status}`;
                board = Chessboard('board', {
                    position: data.fen,
                    draggable: false,
                });
            } else {
                console.error("Error in engine move:", data);
                statusEl.textContent = "Engine move failed.";
            }
        } catch (err) {
            console.error("Error processing engine move:", err);
            statusEl.textContent = "Server error.";
        }
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
            const response = await fetch('/new_game', { method: 'GET' });

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




