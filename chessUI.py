import tkinter as tk

# Taille du plateau de jeu et des cases
BOARD_SIZE = 8
SQUARE_SIZE = 60
# Couleurs des cases du plateau
LIGHT_COLOR = "#EEEED2"
DARK_COLOR = "#769656"

# Symboles des pièces d'échecs en Unicode
PIECE_SYMBOLS = {
    "wp": "♙", "wr": "♖", "wn": "♘", "wb": "♗", "wq": "♕", "wk": "♔",
    "bp": "♟", "br": "♜", "bn": "♞", "bb": "♝", "bq": "♛", "bk": "♚"
}

# Symboles FEN (Forsyth-Edwards Notation) pour les pièces
FEN_SYMBOLS = {
    "wp": "P", "wr": "R", "wn": "N", "wb": "B", "wq": "Q", "wk": "K",
    "bp": "p", "br": "r", "bn": "n", "bb": "b", "bq": "q", "bk": "k"
}

# Position initiale des pièces sur le plateau
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
        self.root.title("Échiquier avec coordonnées externes")

        # Calcul de la taille du canevas
        canvas_width = SQUARE_SIZE * (BOARD_SIZE + 1)
        canvas_height = SQUARE_SIZE * (BOARD_SIZE + 1)

        # Création d'un cadre pour contenir le canevas
        frame = tk.Frame(root)
        frame.pack()

        # Création du canevas pour dessiner le plateau
        self.canvas = tk.Canvas(frame, width=canvas_width, height=canvas_height)
        self.canvas.grid(row=0, column=0)

        self.fen_label = tk.Label(frame, text="FEN :", font=("Arial", 12, "bold"))
        self.fen_label.grid(row=0, column=1, sticky="nw", padx=10)

        self.fen_text = tk.Text(frame, height=3, width=50, font=("Courier", 10))
        self.fen_text.grid(row=0, column=1, sticky="n", padx=10, pady=30)

        # Copie de la position initiale du plateau
        self.board = [row[:] for row in START_POSITION]
        # Dessin du plateau, des pièces et des coordonnées
        self.draw_board()
        self.draw_pieces()
        self.draw_coordinates()
        self.update_fen_display()

        # Ajout d'un bouton pour tourner l'échiquier
        rotate_button = tk.Button(frame, text="Tourner l'échiquier", command=self.rotate_board)
        rotate_button.grid(row=1, column=0, pady=10)

        # Initialisation des variables pour le déplacement des pièces
        self.selected_piece = None
        self.canvas.bind("<Button-1>", self.on_click)

    def draw_board(self):
        # Dessin des cases du plateau
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                # Détermination de la couleur de la case
                color = LIGHT_COLOR if (row + col) % 2 == 0 else DARK_COLOR
                x1 = (col + 1) * SQUARE_SIZE
                y1 = row * SQUARE_SIZE
                x2 = x1 + SQUARE_SIZE
                y2 = y1 + SQUARE_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    def draw_pieces(self):
        # Dessin des pièces sur le plateau
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if piece:
                    symbol = PIECE_SYMBOLS.get(piece, "")
                    x = (col + 1) * SQUARE_SIZE + SQUARE_SIZE // 2
                    y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                    self.canvas.create_text(x, y, text=symbol, font=("Arial", 32))

    def draw_coordinates(self):
        # Dessin des lettres a-h en bas du plateau
        for col in range(BOARD_SIZE):
            letter = chr(ord('a') + col)
            x = (col + 1) * SQUARE_SIZE + SQUARE_SIZE // 2
            y = BOARD_SIZE * SQUARE_SIZE + SQUARE_SIZE // 2
            self.canvas.create_text(x, y, text=letter, font=("Arial", 12, "bold"))

        # Dessin des chiffres 8-1 à gauche du plateau
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

    def rotate_board(self):
        # Inverser les lignes et les colonnes du plateau
        self.board = [row[::-1] for row in self.board[::-1]]
        # Redessiner le plateau et les pièces
        self.canvas.delete("all")
        self.draw_board()
        self.draw_pieces()
        self.draw_coordinates()

    def on_click(self, event):
        # Gestion des clics pour déplacer une pièce
        col = (event.x // SQUARE_SIZE) - 1
        row = event.y // SQUARE_SIZE

        # Vérifier si le clic est dans les limites du plateau
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            if self.selected_piece is None:
                # Premier clic : sélectionner une pièce
                if self.board[row][col]:  # Vérifie qu'il y a une pièce sur la case
                    self.selected_piece = (row, col)
            else:
                # Deuxième clic : déplacer la pièce
                target_row, target_col = row, col
                piece = self.board[self.selected_piece[0]][self.selected_piece[1]]
                self.board[self.selected_piece[0]][self.selected_piece[1]] = ""
                self.board[target_row][target_col] = piece
                self.selected_piece = None

                # Redessiner le plateau et les pièces
                self.canvas.delete("all")
                self.draw_board()
                self.draw_pieces()
                self.draw_coordinates()

if __name__ == "__main__":
    # Création de la fenêtre principale et lancement de l'application
    root = tk.Tk()
    app = ChessUI(root)
    root.mainloop()
