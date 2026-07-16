import { fenIndex, getFENs, setFENIndex } from './state.js'
import { boardFen, getMovableConfig, turnColorFromFen } from './board'


/**
 * Clears the PGN move list.
 */
export function clearPGN() {
    const pgnContainer = document.querySelector(".pgn-container");
    if (!pgnContainer) {
        console.error("clearPGN: PGN container not found.");
        return;
    }
     setFENIndex(0);
    localStorage.setItem("fenIndex", fenIndex);
    pgnContainer.innerHTML = "";
}

/**
 * Updates the PGN move list in the UI.
 */
export function setPGNMoves(pgnString) {
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
export function createPGNButton(text) {
    const button = document.createElement("button");
    button.classList.add("pgn-button");
    button.textContent = text;
    button.fenIndex = fenIndex;

    if (text !== "—") {
        setFENIndex(fenIndex + 1);
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