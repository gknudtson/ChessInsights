
export let fenList = localStorage.getItem("fenList") ? JSON.parse(localStorage.getItem("fenList")) : [];
export let playerColor = "white";
export let fenIndex = localStorage.getItem("fenIndex") ? parseInt(localStorage.getItem("fenIndex")) : 0;
export let currentFen = "start";
export let currentPGN = "";

/**
 * Add given fen to end of fenList.
 */
export function addFEN(fen) {
    fenList.push(fen);
    localStorage.setItem("fenList", JSON.stringify(fenList));
}

/**
 * Return local storage fenList as a JS array.
 */
export function getFENs() {
    return JSON.parse(localStorage.getItem("fenList")) || [];
}

/**
 * Empty fenList.
 */
export function clearFENList() {
    fenList = [];
    localStorage.setItem("fenList", JSON.stringify(fenList));
}

export function setFENIndex(newValue) {
    fenIndex = newValue;
}

export function setCurrentFEN(newValue) {
    currentFen = newValue;
}

export function setCurrentPGN(newValue) {
    currentPGN = newValue;
}

export function setPlayerColor(newValue) {
    playerColor = newValue
}

export function removeLastTwoFENs() {
    fenList = fenList.slice(0, -2);
    localStorage.setItem("fenList", JSON.stringify(fenList));
}