import tkinter as tk
from classes.ChessUI import ChessUI
from PIL import Image, ImageTk
import os

BOARD_SIZE = 8
SQUARE_SIZE = 60

canvas_width = SQUARE_SIZE * (BOARD_SIZE + 1)
canvas_height = SQUARE_SIZE * (BOARD_SIZE + 1)


class MenuUI:
    def __init__(self, root, board_size=BOARD_SIZE, square_size=SQUARE_SIZE):
        self.root = root
        self.root.title("Menu principal")
        self.board_size = board_size
        self.square_size = square_size

        # --- Menu Frame ---
        self.menu_frame = tk.Frame(root, bg="black") 
        self.menu_frame.pack(fill="both", expand=True)

    
        try:
            logo_path = r"..\images\chess.png"
            logo_image = Image.open(logo_path)
            logo_photo = ImageTk.PhotoImage(logo_image)
            self.root.iconphoto(True, logo_photo)
            root.iconbitmap("\images\chess.png")
        except Exception as e:
            print(f"Logo could not be loaded: {e}")

        self.title_label = tk.Label(
            self.menu_frame,
            text="Bienvenue dans mon jeu chess game",
            font=("Arial", 18, "bold"),
            fg="white", bg="black"
        )
        self.title_label.pack(pady=10)

        self.bouton_jouer = tk.Button(
            self.menu_frame,
            text="Jouer", width=20,
            command=self.start_game,
            bg="#222", fg="white", activebackground="#444", activeforeground="white"
        )
        self.bouton_jouer.pack(pady=5)

        self.bouton_quitter = tk.Button(
            self.menu_frame,
            text="Quitter", width=20,
            command=root.quit,
            bg="#222", fg="white", activebackground="#444", activeforeground="white"
        )
        self.bouton_quitter.pack(pady=5)

        # --- Game Frame ---
        self.jeu_frame = tk.Frame(root)
        self.chess_ui = None

    def start_game(self):
        self.menu_frame.pack_forget()
        self.jeu_frame.pack()

        if self.chess_ui is None:
            self.chess_ui = ChessUI(self.root, self.jeu_frame, retour_menu_callback=self.show_menu, board_size=self.board_size,
        square_size=self.square_size,)

    def show_menu(self):
        self.jeu_frame.pack_forget()
        self.menu_frame.pack()
