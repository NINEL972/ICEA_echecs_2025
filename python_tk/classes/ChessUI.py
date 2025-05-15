import tkinter as tk
from tkinter import filedialog
import io
from datetime import date
from PIL import Image, ImageTk
from chess_ICEA_main import *
from classes.Check_pieces import CheckPieces


class ChessUI:
    def __init__(self, main_window, root_frame, board_size, square_size, retour_menu_callback=None):
        self.root = root_frame
        self.main_window = main_window
        self.retour_menu_callback = retour_menu_callback
        self.LIGHT_COLOR = LIGHT_COLOR
        self.DARK_COLOR = DARK_COLOR
        self.PIECE_SYMBOLS = PIECE_SYMBOLS
        self.FEN_SYMBOLS = FEN_SYMBOLS
        self.START_POSITION = START_POSITION
        self.board = [row[:] for row in self.START_POSITION]

        self.BOARD_SIZE = board_size
        self.SQUARE_SIZE = square_size

        self.main_window.title("Échiquier avec coordonnées externes et FEN")

        canvas_width = square_size * (board_size + 1)
        canvas_height = square_size * (board_size + 1)

        frame = tk.Frame(self.root)
        frame.pack()

        self.timer_label = tk.Label(frame, text="Temps : 00:00", font=("Arial", 12, "bold"))
        self.timer_label.grid(row=1, column=0, sticky="n", padx=10, pady=5)

        self.elapsed_seconds = 0 
        self.update_timer() 

        # Initialisation du vérificateur de mouvements
        self.checker = CheckPieces()

        # Chargement du logo
        try:
            logo_path = r"..\images\chess.png"
            logo_image = Image.open(logo_path)
            logo_photo = ImageTk.PhotoImage(logo_image)
            self.main_window.iconphoto(True, logo_photo)
            self.main_window.iconbitmap(r"..\images\chess.png")
        except Exception as e:
            print(f"Logo non chargé : {e}")

        self.canvas = tk.Canvas(frame, width=canvas_width, height=canvas_height)
        self.canvas.grid(row=0, column=0)

        self.fen_label = tk.Label(frame, text="FEN :", font=("Arial", 12, "bold"))
        self.fen_label.grid(row=0, column=1, sticky="nw", padx=10)

        self.fen_text = tk.Text(frame, height=3, width=50, font=("Courier", 10))
        self.fen_text.grid(row=0, column=1, sticky="n", padx=10, pady=30)

        self.flip_button = tk.Button(frame, text="Tourner le plateau", command=self.flip_board)
        self.flip_button.grid(row=1, column=1, sticky="n", padx=10, pady=5)

        # Variables pour le déplacement des pièces
        self.selected_piece = None
        self.canvas.bind("<Button-1>", self.on_click)

        self.draw_board()
        self.draw_pieces()
        self.draw_coordinates()
        self.update_fen_display()

    def draw_board(self):
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                color = self.LIGHT_COLOR if (row + col) % 2 == 0 else self.DARK_COLOR
                x1 = (col + 1) * self.SQUARE_SIZE
                y1 = row * self.SQUARE_SIZE
                x2 = x1 + self.SQUARE_SIZE
                y2 = y1 + self.SQUARE_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    def draw_pieces(self):
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                piece = self.board[row][col]
                if piece:
                    symbol = self.PIECE_SYMBOLS.get(piece, "")
                    x = (col + 1) * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                    y = row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
                    self.canvas.create_text(x, y, text=symbol, font=("Arial", 32))

    def draw_coordinates(self):
        for col in range(self.BOARD_SIZE):
            letter = chr(ord('a') + col)
            x = (col + 1) * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
            y = self.BOARD_SIZE * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
            self.canvas.create_text(x, y, text=letter, font=("Arial", 12, "bold"))

        for row in range(self.BOARD_SIZE):
            number = str(8 - row)
            x = self.SQUARE_SIZE // 2
            y = row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
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
                    fen_row += self.FEN_SYMBOLS.get(piece, "")
            if empty:
                fen_row += str(empty)
            fen_rows.append(fen_row)
        return "/".join(fen_rows) + " w KQkq - 0 1"

    def flip_board(self):
        self.board = [row[::-1] for row in self.board[::-1]]
        self.canvas.delete("all")
        self.draw_board()
        self.draw_pieces()
        self.draw_coordinates()
        self.update_fen_display()

    def on_click(self, event):
        # Gestion des clics pour déplacer une pièce
        col = (event.x // self.SQUARE_SIZE) - 1
        row = event.y // self.SQUARE_SIZE

        # Vérifier si le clic est dans les limites du plateau
        if 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE:
            if self.selected_piece is None:
                # Premier clic : sélectionner une pièce
                if self.board[row][col]:  # Vérifie qu'il y a une pièce sur la case
                    self.selected_piece = (row, col)
            else:
                # Deuxième clic : déplacer la pièce
                target_row, target_col = row, col
                piece = self.board[self.selected_piece[0]][self.selected_piece[1]]
                
                # Vérification du mouvement avec CheckPieces
                if self.checker.verify_move(piece, target_row, target_col):
                    self.board[self.selected_piece[0]][self.selected_piece[1]] = ""
                    self.board[target_row][target_col] = piece
                
                self.selected_piece = None

                # Redessiner le plateau et les pièces
                self.canvas.delete("all")
                self.draw_board()
                self.draw_pieces()
                self.draw_coordinates()
                self.update_fen_display()

    def fen_to_board(self, fen):
        board = []
        rows = fen.split(" ")[0].split("/")
        for row in rows:
            board_row = []
            for char in row:
                if char.isdigit():
                    board_row.extend([""] * int(char))
                else:
                    piece = next((k for k, v in self.FEN_SYMBOLS.items() if v == char), "")
                    board_row.append(piece)
            board.append(board_row)
        return board

    def show_fen(self, fen):
        self.board = self.fen_to_board(fen)
        self.canvas.delete("all")
        self.draw_board()
        self.draw_pieces()
        self.draw_coordinates()
        self.update_fen_display()

    def pgn_to_fens(self, pgn_text):
        fens = []
        game = chess.pgn.read_game(io.StringIO(pgn_text))
        board = game.board()
        fens.append(board.fen())
        for move in game.mainline_moves():
            board.push(move)
            fens.append(board.fen())
        return fens

    def next_move(self):
        if self.current_move_index + 1 < len(self.pgn_moves):
            self.current_move_index += 1
            self.show_fen(self.pgn_moves[self.current_move_index])
            self.update_fen_display()
            self.prev_button.config(state="normal")
            if self.current_move_index == len(self.pgn_moves) - 1:
                self.next_button.config(state="disabled")

    def prev_move(self):
        if self.current_move_index > 0:
            self.current_move_index -= 1
            self.show_fen(self.pgn_moves[self.current_move_index])
            self.update_fen_display()
            self.next_button.config(state="normal")
            if self.current_move_index == 0:
                self.prev_button.config(state="disabled")

    def start_game(self):
        self.root.mainloop()

    def update_timer(self):
        minutes = self.elapsed_seconds // 60
        seconds = self.elapsed_seconds % 60
        time_str = f"Temps : {minutes:02d}:{seconds:02d}"
        self.timer_label.config(text=time_str)
        self.elapsed_seconds += 1
        self.root.after(1000, self.update_timer)