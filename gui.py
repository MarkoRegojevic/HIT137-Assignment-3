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
        self.solve_button.grid(row=0, column=4, padx=5) 

    #  This block shows the score of the game, including moves and tiles left to solve
        score_frame = tk.Frame(self.window)
        score_frame.pack(pady=5)

        self.moves_label = tk.Label(
            score_frame,
            text="Moves: 0"
        )
        self.moves_label.grid(row=0, column=0, padx=20)

        self.tiles_label = tk.Label(
            score_frame,
            text="Tiles Incorrect: 0"
        )
        self.tiles_label.grid(row=0, column=1, padx=20)

        self.hints_label = tk.Label(
            score_frame,
            text="Hints Used: 0 / 3"
        )
        self.hints_label.grid(row=0, column=2, padx=20) 
#   section where the two images go
        image_frame = tk.Frame(self.window)
        image_frame.pack(pady=10)
        original_text = tk.Label(
            image_frame,
            text="Original Image"
        )
        original_text.grid(row=0, column=0, padx=20)
        puzzle_text = tk.Label(
            image_frame,
            text="Puzzle Image"
        )
        puzzle_text.grid(row=0, column=1, padx=20)



#Original image area 
        self.original_image_label = tk.Label(
            image_frame, 
            text="Load and image" 
            width=50, 
            height=25,
            relief="solid"
        )
        self.original_label.grid(
            row=1
            column=20
            pady=5
        )

#The transformed image area 
        self.puzzle_label = tk.Label(
            image_frame, 
            text="Puzzle will appear here",
            width=50,
            height=25,
            relief="solid"
        )
        self.puzzle_label.grid(
            row=1,
            column=1,
            padx=20,
            pady=5
        )
#The mouse controls for the puzzle image, allowing the user to select and move tiles 

        self.puzzle_label.bind(
            "<Button-1>",
            self.left_click
        )

        self.puzzle_label.bind(
            "<Button-3>",
            self.right_click
        )

        self.puzzle_label.bind(
            "<Shift-Button-1>",
            self.shift_left_click
        ) 

#This part will let the user choose an image form thier computer and load it into the game 
    def choose_image(self):


        file_path = filedialog.askopenfilename(
            title="Choose an image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("PNG files", "*.png"),
                ("BMP files", "*.bmp")
            ]
        )
#If the cancel button is pressed 
    
        if file_path == "":
            return
        try:
            size = self.grid_size.get() 

#Loads and prepares the image for the puzzle game 
            image = self.image_processor.load_image(file_path)

            if image is None:
                messagebox.showerror(
                    "Error",
                    "The image could not be loaded."
                )
                return
            image = self.image_processor.resize_image(image) 

            image = self.image_processor.prepare_grid(
                image,
                size
            )
#Makes a new puzzle 
            self.puzzle = Puzzle(
                image,
                size,
                self.image_processor
            )

            self.puzzle.create_tiles()
            self.puzzle.scramble()

#Resets everything for the new image
            self.moves = 0
            self.hints_used = 0
            self.selected_tile = None
            self.game_finished = False

            self.hint_button.config(state="normal")

            self.update_images()
            self.update_score()
        except Exception:

            messagebox.showerror(
                "Error",
                "There was a problem loading the image."
            )

#Updates both images shown on the screen
    def update_images(self):

        if self.puzzle is None:
            return

        original_image = self.puzzle.get_original_image()

        puzzle_image = self.puzzle.get_display_image(
            self.selected_tile
        )
        self.show_original_image(original_image)
        self.show_puzzle_image(puzzle_image)
 #Shows the original image on the left
    def show_original_image(self, image):

        image = self.convert_image(image)

        self.original_photo = ImageTk.PhotoImage(image)

        self.original_label.config(
            image=self.original_photo,
            text=""
        )
#mShows the puzzle image on the right
    def show_puzzle_image(self, image):

        image = self.convert_image(image)

        self.puzzle_photo = ImageTk.PhotoImage(image)

        self.puzzle_label.config(
            image=self.puzzle_photo,
            text=""
        )
#Changes an opencv image so tkinter can display it
    def convert_image(self, image):

        image = self.image_processor.convert_to_rgb(image)

        image = Image.fromarray(image)
        return image 

    
#Works out which tile was clicked 
    def get_clicked_tile(self, event):
        if self.puzzle is None:
            return None
        image_width = self.puzzle.get_width()
        image_height = self.puzzle.get_height()


        if event.x < 0 or event.y < 0:
            return None

        if event.x >= image_width or event.y >= image_height:
            return None

        tile_width = image_width // self.grid_size.get()
        tile_height = image_height // self.grid_size.get()

        column = event.x // tile_width
        row = event.y // tile_height

        return row, column
 #Left lcikc slects a title or swaps tiles 
    def left_click(self, event):
        if self.puzzle is None or self.game_finished:
            return
        tile = self.get_clicked_tile(event)
        if tile is None:
            return

        if self.selected_tile is None:
            self.selected_tile = tile
            self.update_images()
            return
        
        if self.selected_tile == tile:
            self.selected_tile = None
            self.update_images()
            return

        self.puzzle.swap_tiles(
            self.selected_tile,
            tile           
        )

        self.selected_tile = None
        self.move_made()


#Right click rotates a tile 
    def right_click(self, event):
        if self.puzzle is None or self.game_finished:
            return
        tile = self.get_clicked_tile(event)
        if tile is None:
            return

        self.puzzle.rotate_tile(tile)
        self.move_made() 

#Shift and left clikc flips a tile 
    def shift_left_click(self, event):
        if self.puzzle is None or self.game_finished:
            return
        tile = self.get_clicked_tile(event)
        if tile is None:
            return

        self.puzzle.flip_tile(tile)
        self.move_made()

#Runs after the user has made a move. 
    def move_made(self): 
        self.moves += 1 
        self.puzle.clear_hint()
        self.update_images()
        self.update_score()
        self.check_finished() 

        def update_score(self):
            if self.puzzle is None:
                self.tiles_left = 0

            else: 
                self.tiles_left = self.puzzle.count_incorrect_tiles()

            self.moves_label.config(
                text="Moves: " + str(self.moves)
            )
            self.tiles_label.config(
                text="Tiles Incorrect: " + str(self.tiles_left)
            )
            self.hints_label.config(
                text="Hints Used: " + str(self.hints_used) + " / 3" 
            )

            