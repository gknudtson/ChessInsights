export async function postMove(fromSquare, toSquare) {
    const response = await fetch('/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ fromSquare, toSquare })
    });
    return response.json();
}

export async function fetchEngineMove() {
    const response = await fetch('/engine_move', { method: 'GET' });
    return response.json();
}

export async function postUndo() {
    const response = await fetch('/undo', { method: 'GET' });
    return response.json();
}