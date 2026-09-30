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