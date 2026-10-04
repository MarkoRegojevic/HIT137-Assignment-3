import cv2
import numpy as np

class ImageProcessor:

    def __init__(self, max_width=500, max_height=500):

        self.max_width = max_width
        self.max_height = max_height


# load image from file
    def load_image(self, file_path):

        image = cv2.imread(file_path)

        if image is None:
            raise ValueError("Image could not be loaded. Please check the file path.")

        return image


# resize image to fit within max_width and max_height while maintaining aspect ratio

    def resize_image(self, image):

        height, width = image.shape[:2]

        width_scale = self.max_width / width
        height_scale = self.max_height / height

        scale = min(
            width_scale,
            height_scale,
            1
        )

        new_width = int(width * scale)
        new_height = int(height * scale)

        return cv2.resize(
        image,
        (new_width, new_height),
        interpolation=cv2.INTER_AREA
    )


    # pads image so that the grid divides evenly

    def pad_image(self, image, grid_size):

        height, width = image. shape[:2]

        size = max(height, width)

        if size % grid_size != 0:
            size += grid_size - (size % grid_size)

        extra_width = size - width
        extra_height = size - height

        left = extra_width // 2
        right = extra_width - left

        top = extra_height // 2
        bottom = extra_height - top

        return cv2.copyMakeBorder(
            image,
            top,
            bottom,
            left,
            right,
            cv2.BORDER_CONSTANT,
            value=(0, 0, 0)
        )

# load, resize and pad image from file

    def prepare_image(self, file_path, grid_size):

        if grid_size not in [3, 4, 5]:
            raise ValueError("Grid size must be 3, 4 or 5")

        image = self.load_image(
            file_path
        )

        image= self.resize_image(
            image
        )

        image= self.pad_image(
            image,
            grid_size
        )

        return image

# splits the image into tiles

    def split_image(self, image, grid_size):

        tiles=[]

        height, width = image.shape[:2]

        tile_height = height // grid_size
        tile_width = width // grid_size

        for row in range(grid_size):

            for column in range(grid_size):

                y1 = row * tile_height
                y2 = y1 + tile_height

                x1 = column * tile_width
                x2 = x1 + tile_width

                tile = image[
                    y1:y2,
                    x1:x2
                ].copy()

                tiles.append(tile)

        return tiles

# reassemble tiles into one complete image

    def reassemble_image(self, tiles, grid_size):

        rows = []

        for row in range(grid_size):

            row_tiles = []

            for column in range(grid_size):

                index = (
                    row * grid_size
                    + column
                )

                row_tiles.append(
                    tiles[index]
                )

            rows.append(
                cv2.hconcat(row_tiles)
            )

        return cv2.vconcat(rows)

# rotates tiles 90 180 270 degrees

    def rotate_tile(self, tile, angle):

        if angle == 90:

            return cv2.rotate(
                tile,
                cv2.ROTATE_90_CLOCKWISE
            )

        elif angle == 180:

            return cv2.rotate(
                tile,
                cv2.ROTATE_180
            )

        elif angle == 270:

            return cv2.rotate(
                tile,
                cv2.ROTATE_90_COUNTERCLOCKWISE
            )

        return tile.copy()

# flips a tile

    def flip_tile(self, tile, direction):

        if direction == "horizontal":
            return cv2.flip(tile, 1)

        elif direction == "vertical":
            return cv2.flip(tile, 0)

        return tile.copy()


# draw grind lines on the image

    def draw_grid(self, image, grid_size):

        height, width = image.shape[:2]

        tile_width = width // grid_size
        tile_height = height // grid_size

        for i in range(1, grid_size):

            cv2.line(
                image,
                (i*tile_width, 0),
                (i*tile_width, height),
                (180, 180, 180),
                1
            )

            cv2.line(
                image,
                (0, i*tile_height),
                (width, i*tile_height),
                (180, 180, 180),
                1
            )

        return image


# draw coloured box around one tile

    def draw_tile_box(
        self,
        image,
        index,
        grid_size,
        colour
    ):

        height, width = image.shape[:2]

        tile_width = width // grid_size
        tile_height = height // grid_size

        row = index // grid_size
        column = index % grid_size

        x1 = column * tile_width
        y1 = row * tile_height

        x2 = x1 + tile_width - 1
        y2 = y1 + tile_height - 1

        cv2.rectangle(
            image,
            (x1, y1),
            (x2, y2),
            colour,
            3
        )


# draw the hint circle

    def draw_circle(
            self,
            image,
            index,
            grid_size
    ):

        height, width = image.shape[:2]

        tile_width = width // grid_size
        tile_height = height // grid_size

        row = index // grid_size
        column = index % grid_size

        centre = (
            column * tile_width + tile_width // 2,
<<<<<<< HEAD
            row * tile_height + tile_height // 2

        )

        cv2.circle(
            image,
            centre,
            min(tile_width, tile_height) // 5,
            (255, 0, 0),
            3
        )
=======
        row * tile_height + tile_height // 2
        )

        cv2.circle(
            image,
            centre,
            min(tile_width, tile_height) // 5,
            (255, 0, 0),
            3
        )

>>>>>>> c4ceec03dc6bf01383169fc606731b16c7184084


# convert openvc colours (rgb)

    def convert_to_rgb(self, image):

        return cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

    