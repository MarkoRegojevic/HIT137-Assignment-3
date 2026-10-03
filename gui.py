# gui for the image puzzle game 

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox 

from PIL import Image, ImageTk 
from image_processor import ImageProcessor  

class PuzzleGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Image Puzzle Game")
        self.window.geometry("1100x700")
        self.image_processor = ImageProcessor()
        self.puzzle = None
        self.original_image = None
        self.original_photo = None
        self.puzzle_photo = None
        self.grid_size = tk.IntVar(value=3)
        self.moves = 0
        self.tiles_left = 0
        self.hints_used = 0
        self.selected_tile = None
        self.hint_current = None
        self.hint_home = None
        self.game_finished = False
        self.create_widgets()

#Makes all of the buttons, labels and image areas
    def create_widgets(self):
        tk.Label(
            self.window,
            text="Image Puzzle Game",
            font=("Arial", 18)
        ).pack(pady=10)
        controls = tk.Frame(self.window)
        controls.pack(pady=10)
        tk.Button(
            controls,
            text="Load Image",
            command=self.choose_image
        ).grid(row=0, column=0, padx=5)

        tk.Label(
            controls,
            text="Grid Size:"
        ).grid(row=0, column=1, padx=5)
        tk.OptionMenu(
            controls,
            self.grid_size,
            3, 4, 5
        ).grid(row=0, column=2, padx=5)
        self.hint_button = tk.Button(
            controls,
            text="Hint",
            command=self.use_hint,
            state="disabled"
        )
        self.hint_button.grid(row=0, column=3, padx=5)

        self.solve_button = tk.Button(
            controls,
            text="Solve",
            command=self.solve_puzzle,
            state="disabled"
        )
        self.solve_button.grid(row=0, column=4, padx=5)

        score_frame = tk.Frame(self.window)
        score_frame.pack(pady=5)

        self.moves_label = tk.Label(score_frame, text="Moves: 0")
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

        image_frame = tk.Frame(self.window)
        image_frame.pack(pady=10)

        tk.Label(
            image_frame,
            text="Original Image"
        ).grid(row=0, column=0, padx=20)

        tk.Label(
            image_frame,
            text="Puzzle Image"
        ).grid(row=0, column=1, padx=20)

        self.original_image_label = tk.Label(
            image_frame,
            text="Load an image",
            relief="solid"
        )
        self.original_image_label.grid(
            row=1,
            column=0,
            padx=20,
            pady=5
        )

        self.puzzle_label = tk.Label(
            image_frame,
            text="Puzzle will appear here",
            relief="solid"
        )
        self.puzzle_label.grid(
            row=1,
            column=1,
            padx=20,
            pady=5
        )

        self.puzzle_label.bind("<Button-1>", self.left_click)
        self.puzzle_label.bind("<Button-3>", self.right_click)
        self.puzzle_label.bind(
            "<Shift-Button-1>",
            self.shift_left_click
        )

#This part will let the user choose an image form thier computer and load it into the game 
    def choose_image(self):
        file_path = filedialog.askopenfilename(
            title="Choose an image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp")
            ]
        )

        if file_path == "":
            return
        try:
            size = self.grid_size.get()

            image = self.image_processor.prepare_image(
                file_path,
                size
            )
            self.original_image = image.copy()

            tile_images = self.image_processor.split_image(
                image,
                size
            )
            tiles = []
            for i in range(len(tile_images)):
                tiles.append(
                    Tile(tile_images[i], i, i)
                )
            self.puzzle = PuzzleBoard(size)
            self.puzzle.load_tiles(tiles)
            self.puzzle.scramble()

            self.moves = 0
            self.tiles_left = 0
            self.hints_used = 0

            self.selected_tile = None
            self.hint_current = None
            self.hint_home = None
            self.game_finished = False

            self.hint_button.config(state="normal")
            self.solve_button.config(state="normal")

            self.update_images()
            self.update_score()
        except Exception as error:
            print(error)
            messagebox.showerror(
                "Error",
                "There was a problem loading the image."
            ) 
            
#This will update the original and puzzle images 
    def update_images(self):
        if self.puzzle is None:
            return

        original_image = self.original_image.copy()
        puzzle_tiles = []

        for tile in self.puzzle.tiles:
            tile_image = tile.image.copy()

            if tile.is_flipped_h:
                tile_image = self.image_processor.flip_tile(
                    tile_image,
                    "horizontal"
                )

            if tile.is_flipped_v:
                tile_image = self.image_processor.flip_tile(
                    tile_image,
                    "vertical"
                )

            if tile.rotation != 0:
                tile_image = self.image_processor.rotate_tile(
                    tile_image,
                    tile.rotation
                )

            puzzle_tiles.append(tile_image)
        puzzle_image = self.image_processor.reassemble_image(
            puzzle_tiles,
            self.grid_size.get()
        )
        puzzle_image = self.image_processor.draw_grid(
            puzzle_image,
            self.grid_size.get()
        )
        for tile in self.puzzle.tiles:
            if tile.is_correct():
                self.draw_tick(
                    puzzle_image,
                    tile.current_pos
                )

        if self.selected_tile is not None:
            index = self.tile_to_index(
                self.selected_tile
            )
            self.draw_selection(
                puzzle_image,
                index
            )

        if self.hint_current is not None:
            self.draw_hint(
                puzzle_image,
                self.hint_current
            )
            self.draw_hint(
                original_image,
                self.hint_home
            )

        self.show_image(
            original_image,
            self.original_image_label,
            "original"
        )

        self.show_image(
            puzzle_image,
            self.puzzle_label,
            "puzzle"
        ) 
#This will display the selected image in tinker 
    def show_image(self, image, label, image_type):
        image = self.image_processor.convert_to_rgb(image)
        image = Image.fromarray(image)
        photo = ImageTk.PhotoImage(image)
        label.config(
            image=photo,
            text=""
        )
        if image_type == "original":
            self.original_photo = photo
        else:
            self.puzzle_photo = photo 
#Works out which tile was clicked 
    def get_clicked_tile(self, event):
        if self.puzzle is None:
            return None
        height, width = self.original_image.shape[:2]
        if event.x < 0 or event.y < 0:
            return None
        if event.x >= width or event.y >= height:
            return None
        size = self.grid_size.get()
        tile_width = width // size
        tile_height = height // size
        column = event.x // tile_width
        row = event.y // tile_height
        return row, column 

#converts the columnn and row int a index 
    def tile_to_index(self, tile):
        row, column = tile

        return (
            row * self.grid_size.get()
            + column
        )

#This block will select or swaps tiles
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
        first = self.tile_to_index(
            self.selected_tile
        )

        second = self.tile_to_index(tile)
        self.puzzle.swap_tiles(
            first,
            second
        )
        self.selected_tile = None
        self.move_made()
#THis function will rotate tiles when pressed 
    def right_click(self, event):
        if self.puzzle is None or self.game_finished:
            return

        tile = self.get_clicked_tile(event)

        if tile is None:
            return

        self.puzzle.rotate_tile(
            self.tile_to_index(tile)
        )

        self.move_made() 
#flips tile horizontally when the shift button and left mouse button are pressed 
    def shift_left_click(self, event):
        if self.puzzle is None or self.game_finished:
            return
        tile = self.get_clicked_tile(event)
        if tile is None:
            return
        self.puzzle.flip_tile(
            self.tile_to_index(tile),
            "h"
        )
        self.move_made()

    def move_made(self):
        self.moves = self.puzzle.move_count

        self.hint_current = None
        self.hint_home = None

        self.update_images()
        self.update_score()
        self.check_finished()

    def update_score(self):
        if self.puzzle is None:
            self.tiles_left = 0
        else:
            self.tiles_left = (
                self.puzzle.get_incorrect_count()
            )
        self.moves_label.config(
            text="Moves: " + str(self.moves)
        )

        self.tiles_label.config(
            text="Tiles Incorrect: "
            + str(self.tiles_left)
        )

        self.hints_label.config(
            text="Hints Used: "
            + str(self.hints_used)
            + " / 3"
        )

#This section will give player a hint
    def use_hint(self):
        if self.puzzle is None or self.game_finished:
            return
        if self.hints_used >= 3:
            self.hint_button.config(
                state="disabled"
            )
            return
        hint = self.puzzle.get_hint()
        if hint is None:
            messagebox.showinfo(
                "Hint",
                "There are no incorrect tiles."
            )
            return
        self.hint_current = hint[0]
        self.hint_home = hint[1]
        self.hints_used += 1
        if self.hints_used >= 3:
            self.hint_button.config(
                state="disabled"
            )
        self.update_images()
        self.update_score()

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

        self.original_image_label.config(
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
        self.puzzle.clear_hint()
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
#it will give the player a hint if they have not used all of their hints 
    def use_hint(self):
        if self.puzzle is None or self.game_finished:
            return
        if self.hints_used >= 3: 
            self.hint_button.config(state="disabled") 
            return
        hint_found = self.puzzle.make_hint() 
        if hint_found:
            self.hints_used += 1
            if self.hints_used >= 3:
                self.hint_button.config(state="disabled")
            self.update_images()
            self.update_score() 

        else: 
            messagebox.showinfo(
                "Hint",
                "There are no incorrect tiles."
            )
#Solves the puzzle and ends the game 
    def solve_puzzle(self):

        if self.puzzle is None:
            return

        self.puzzle.solve_puzzle() 

        self.moves = 0
        self.selected_tile = None
        self.game_finished = True
        self.update_images()
        self.update_score()

        messagebox.showinfo(
            "Solved",
            "The puzzle has been solved."
        )
#Checks if the player completed the puzzle and ends the game if they have 
    def check_finished(self):
        if self.puzzle is None:
            return
        if self.puzzle.is_solved():
            self.game_finished = True
            messagebox.showinfo(
                "Congratulations",
                "You have solved the puzzle!"
            )
#Activate the tinker program 
    def run(self):
        self.window.mainloop()