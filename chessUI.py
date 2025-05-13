import tkinter as tk

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

class ChessUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Échiquier avec coordonnées externes et FEN")

        canvas_width = SQUARE_SIZE * (BOARD_SIZE + 1)
        canvas_height = SQUARE_SIZE * (BOARD_SIZE + 1)

        frame = tk.Frame(root)
        frame.pack()

        self.canvas = tk.Canvas(frame, width=canvas_width, height=canvas_height)
        self.canvas.grid(row=0, column=0)

        self.fen_label = tk.Label(frame, text="FEN :", font=("Arial", 12, "bold"))
        self.fen_label.grid(row=0, column=1, sticky="nw", padx=10)

        self.fen_text = tk.Text(frame, height=3, width=50, font=("Courier", 10))
        self.fen_text.grid(row=0, column=1, sticky="n", padx=10, pady=30)

        self.board = [row[:] for row in START_POSITION]
        self.draw_board()
        self.draw_pieces()
        self.draw_coordinates()
        self.update_fen_display()

    def draw_board(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = LIGHT_COLOR if (row + col) % 2 == 0 else DARK_COLOR
                x1 = (col + 1) * SQUARE_SIZE
                y1 = row * SQUARE_SIZE
                x2 = x1 + SQUARE_SIZE
                y2 = y1 + SQUARE_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    def draw_pieces(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if piece:
                    symbol = PIECE_SYMBOLS.get(piece, "")
                    x = (col + 1) * SQUARE_SIZE + SQUARE_SIZE // 2
                    y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                    self.canvas.create_text(x, y, text=symbol, font=("Arial", 32))

    def draw_coordinates(self):
        # Lettres a-h en bas
        for col in range(BOARD_SIZE):
            letter = chr(ord('a') + col)
            x = (col + 1) * SQUARE_SIZE + SQUARE_SIZE // 2
            y = BOARD_SIZE * SQUARE_SIZE + SQUARE_SIZE // 2
            self.canvas.create_text(x, y, text=letter, font=("Arial", 12, "bold"))

        # Chiffres 8-1 à gauche
        for row in range(BOARD_SIZE):
            number = str(8 - row)
            x = SQUARE_SIZE // 2
            y = row * SQUARE_SIZE + SQUARE_SIZE // 2
            self.canvas.create_text(x, y, text=number, font=("Arial", 12, "bold"))

    def update_fen_display(self):
        fen = self.board_to_fen()
        self.fen_text.delete("1.0", tk.END)
        self.fen_text.insert(tk.END, fen)

    def board_to_fen(self):
        fen_rows = []
        for row in self.board:
            fen_row = ""
            empty = 0
            for piece in row:
                if piece == "":
                    empty += 1
                else:
                    if empty:
                        fen_row += str(empty)
                        empty = 0
                    fen_row += FEN_SYMBOLS.get(piece, "")
            if empty:
                fen_row += str(empty)
            fen_rows.append(fen_row)
        return "/".join(fen_rows) + " w KQkq - 0 1"

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessUI(root)
    root.mainloop()