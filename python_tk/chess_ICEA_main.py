import tkinter as tk
from classes.ChessUI import ChessUI

BOARD_SIZE = 8
SQUARE_SIZE = 60
LIGHT_COLOR = "#EEEED2"
DARK_COLOR = "#769656"

PIECE_SYMBOLS = {
    "wp": "♙", "wr": "♖", "wn": "♘", "wb": "♗", "wq": "♕", "wk": "♔",
    "bp": "♟", "br": "♜", "bn": "♞", "bb": "♝", "bq": "♛", "bk": "♚"
}

FEN_SYMBOLS = {
    "wp": "P", "wr": "R", "wn": "N", "wb": "B", "wq": "Q", "wk": "K",
    "bp": "p", "br": "r", "bn": "n", "bb": "b", "bq": "q", "bk": "k"
}

START_POSITION = [
    ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
    ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
    ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]
]

if __name__ == "__main__" : 
    root = tk.Tk()
    app = ChessUI(root, BOARD_SIZE, SQUARE_SIZE, LIGHT_COLOR, DARK_COLOR, PIECE_SYMBOLS, FEN_SYMBOLS, START_POSITION)
    root.mainloop()