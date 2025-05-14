import tkinter as tk 
from ChessUI import ChessUI 

# Définition des constantes pour l'échiquier
BOARD_SIZE = 8  
SQUARE_SIZE = 60 

# Calcul de la taille du canevas en fonction de la taille des cases et de l'échiquier
canvas_width = SQUARE_SIZE * (BOARD_SIZE + 1)
canvas_height = SQUARE_SIZE * (BOARD_SIZE + 1)

class MenuUI:
    def __init__(self, root):
        self.root = root  
        self.root.title("Menu principal") 

        # --- Menu Frame ---
        self.menu_frame = tk.Frame(root, bg="black") 
        self.menu_frame.pack(fill="both", expand=True) 

        # Titre du menu
        self.title_label = tk.Label(
            self.menu_frame,
            text="Bienvenue dans mon jeu chess game", 
            font=("Arial", 18, "bold"),
            fg="white", bg="black"
        )
        self.title_label.pack(pady=10)

        # Bouton "Jouer"
        self.bouton_jouer = tk.Button(
            self.menu_frame,
            text="Jouer", width=20,  
            command=self.start_game, 
            bg="#222", fg="white", activebackground="#444", activeforeground="white"
        )
        self.bouton_jouer.pack(pady=5)

        # Bouton "Quitter"
        self.bouton_quitter = tk.Button(
            self.menu_frame,
            text="Quitter", width=20,  
            command=root.quit,  
            bg="#222", fg="white", activebackground="#444", activeforeground="white"
        )
        self.bouton_quitter.pack(pady=5)  

        # --- Game Frame (vide au départ) ---
        self.jeu_frame = tk.Frame(root)  
        self.chess_ui = None  
    def start_game(self):
        self.menu_frame.pack_forget()  
        self.jeu_frame.pack() 

        if self.chess_ui is None:
            self.chess_ui = ChessUI(self.root, self.jeu_frame, retour_menu_callback=self.show_menu)

    def show_menu(self):
        self.jeu_frame.pack_forget()
        self.menu_frame.pack(fill="both", expand=True)
