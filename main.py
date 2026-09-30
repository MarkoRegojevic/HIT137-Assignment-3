# Image Puzzle Game

# gets the GUI class from the gui file
from gui import PuzzleGUI

# this function starts the puzzle program
def main():

    # makes the main puzzle window
    app = PuzzleGUI()

    # starts the program
    app.run()

# runs the program
if __name__ == "__main__":
    main()