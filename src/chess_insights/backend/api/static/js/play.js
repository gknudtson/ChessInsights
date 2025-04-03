localStorage.setItem("playerColor", "white");
localStorage.setItem("currentFen", "start");
localStorage.removeItem("fenList");
localStorage.removeItem("fenIndex");
var currentPGN = '';

/**
 * Sets the board to a user-inputted FEN.
 */
async function setFen() {
    const fenInput = document.getElementById("userInput").value.trim();
    const color = fenInput.includes(" w ") ? "white" : "black";
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

        // If successful, the server will return a redirect to /game
        if (response.redirected) {
            // Store values in localStorage
            localStorage.setItem("playerColor", color);
            localStorage.setItem("currentFen", fenInput);
            // Redirect to /game
            window.location.href = response.url;
        } else {
            const data = await response.json();
            alert(`Error: ${data.error || "Invalid FEN entered!"}`);
        }
    } catch (error) {
        console.error("Error setting FEN:", error);
        alert("Failed to update board. Please check your FEN.");
    }
}

async function renderGame(color) {
    if (color === 'random') {
        color = Math.random() < 0.5 ? "white" : "black";
    }

    const response = await fetch('/start_game', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({side: color})
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem("playerColor", data.color);
        localStorage.setItem("currentFen", data.fen);
        window.location.href = "/game";
    } else {
        const error = await response.json();
        alert("Failed to start game: " + error.message);
    }
}
