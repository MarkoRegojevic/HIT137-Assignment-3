class Tile:
    def __init__(self, image, home_pos, current_pos):
        self.image = image
        self.home_pos = home_pos
        self.current_pos = current_pos
        self.rotation = 0
        self.is_flipped_h = False
        self.is_flipped_v = False

    def is_correct(self):
        return (self.current_pos == self.home_pos and
                self.rotation == 0 and
                self.is_flipped_h == False and
                self.is_flipped_v == False)


class PuzzleBoard:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.tiles = []
        self.move_count = 0
        self.hints_remaining = 3

    def load_tiles(self, tiles_list):
        self.tiles = tiles_list
        self.move_count = 0
        self.hints_remaining = 3

    def swap_tiles(self, index1, index2):
        self.tiles[index1], self.tiles[index2] = self.tiles[index2], self.tiles[index1]
        self.tiles[index1].current_pos = index1
        self.tiles[index2].current_pos = index2
        self.move_count += 1

    def rotate_tile(self, index):
        self.tiles[index].rotation += 90
        if self.tiles[index].rotation >= 360:
            self.tiles[index].rotation -= 360
        self.move_count += 1

    def flip_tile(self, index, direction='h'):
        if direction == 'h':
            self.tiles[index].is_flipped_h = not self.tiles[index].is_flipped_h
        else:
            self.tiles[index].is_flipped_v = not self.tiles[index].is_flipped_v
        self.move_count += 1

