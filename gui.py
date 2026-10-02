# gui for the image puzzle game 

import tkinter as tk
from tinker import filedialog
from tinker import messagebox 

from PTL import Puzzle
from image_processing import ImageProcessing 

class PuzzleGUI:
    def __init__(self):
        #this will make the main window for the puzzle game 
        self.window = tk.Tk() 
        self.windown.title("Image Puzzle Game")
        self.windown.gemometry("1100x700")

        self.image_processor = ImageProcessor() 

        self.puzzle = None 

        self.original_photo = None 
        self.puzzle_photo = None 

        self.grid_szie = tk.IntVar() 
        self.grid_size.set(3)

        self.moves = 0
        self.titles_left = 0 
        self.hints_used = 0 

        self.selected_title = None

        self.game_finished = False

        self.create_widgets() 

    # makes all of the buttons, labels and image areas
    def create_widgets(self):

        title_label = tk.Label(
            self.window,
            text="Image Puzzle Game",
            font=("Arial", 18)
        )
        title_label.pack(pady=10)

        # top section for buttons and grid size 
        control_frame = tk.Frame(self.window)
        control_frame.pack(pady=10)

        load_button = tk.Button(
            control_frame,
            text="Load Image",
            command=self.load_image
        )
        load_button.grid(row=0, column=0, padx=5)

        grid_label = tk.Label(
            control_frame,
            text="Grid Size:"  
        )
        grid_label.grid(row=0, column=1, padx=5)

        grid_menu = tk.OptionMenu(
            control_frame,
            self.grid_size,
            3,
            4,
            5
        )
        grid_menu.grid(row=0, column=2, padx=5)

        self.hit_button = tk.Button(
            control_frame,
            text="Hint",
            command=self.use_hint,
        )
        self.hint_button.grid(row=0, column=3, padx=5)

        self.solve_button = tk.Button(
            control_frame,
            text="Solve",
            command=self.solve_puzzle
        )

