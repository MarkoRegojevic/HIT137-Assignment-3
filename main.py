#Image Puzzle Game
#Gets the GUI class from the gui file
from gui import PuzzleGUI

#This function starts the puzzle program
def main():

#Makes the main puzzle window
    app = PuzzleGUI()

    #Starts the program
    app.run()
#Runs the program
if __name__ == "__main__":
    main() 