from enum import Enum


class GameStatus(Enum):
    ONGOING = "Ongoing"
    CHECKMATE = "Checkmate"
    STALEMATE = "Stalemate"
    DRAW_50_MOVE = "Draw (50-move rule)"
    DRAW_INSUFFICIENT_MATERIAL = "Draw (Insufficient Material)"
    DRAW_REPETITION = "Draw (Threefold Repetition)"
