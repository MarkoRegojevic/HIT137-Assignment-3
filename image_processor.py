import cv2

class ImageProcessor:

    def __init__(self, max_width=600, max_height=600):
        self.max_width = max_width
        self.max_height = max_height


# load image from file

def resize_image(self, image):

    height, width = image.shape[0:2]

    width_scale = self.max_width / width
    height_scale = self.max_height / height

    scale = min(
        width_scale,
        height_scale,
        1
    )

    new_width = int(width * scale)
    new_height = int(height * scale)

    resized_image = cv2.resize(
        image,
        (new_width, new_height),
        interpolation=cv2.INTER_AREA
    )

    return resized_image


# pads image so that the grid divides evenly
# the image is maade square so rotated tiles still fit in the grid

def pad_image(self, image, grid_size):

    height, width = image. shape[0:2]

    size = max(height, width)

    remainder = size % grid_size

    if remainder != 0:
        size = size + (
            grid_size - remainder
        )

    extra_width = size - width
    extra_height = size - height

    left=extra_width // 2
    right=extra_width - left

    top=extra_height // 2
    bottom=extra_height - top

    padded_image = cv2.copyMakeBorder(
        image,
        top,
        bottom,
        left,
        right,
        cv2.BORDER_CONSTANT,
        value=(0, 0, 0)

    )

    return padded_image 

# load, resize and pad image from file

def prepare_image(self, file_path, grid_size):

    if grid_size not in [3, 4, 5]:
        raise ValueError(
            "Grid size must be 3, 4 or 5"

        )

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

# split the image into tiles

def split_image(self, image, grid_size):

    tiles=[]

    height, width = image.shape[0:2]

    tile_height = (
        height // grid_size
    )

    title_width = (
        width // grid_size

    )

    for row in range(grid_size):

        for column in range(grid_size):

            y1 = row * tile_height
            y2 = y1 + tile_height

            x1 = column * title_width
            x2 = x1 + title_width

            title = image[
                y1:y2
                x1:x2

            ].copy()

            titles.append(title)

    return tiles

# reassemble tiles into one complete image

def reassemble_image(
        self,
        titles,
        grid_size
    
):

    rows = []

    for row in range(grind_size):

        row_titles = []

        for column in range(grid_size):

            index = (
                row * grid_size
                + column
            )

            row_titles.append(
                titles[index]
            )

        combined_row = cv2.hconcat(
            row_tiles
        )

        rows.append(
            combined_row
        )

    complete_image = cv2.vconcat(
        rows
    )

    return complete_image

# swap two tiles in the list

def swap_titles(
    self,
    tiles,
    first_index,
    second_index

):

    temp = tiles[first_index]
    
    tiles[first_index] = \
        tiles[second_index]

    tiles[second_index] = temp

    return tiles

# rotate tile 90 degrees clockwise
# angle can be 0, 90, 180, 270

def rotate_tile(
        self,
        tile,
        angle
):

    if angle == 90:

        rotated_tile = cv2.rotate(
            tile,
            cv2.ROTATE_90_CLOCKWISE
        )

    elif angle == 180:

        rotated_tile == cv2.rotate(
            tile,
            cv2.ROTATE_180
        )

    elif angle == 270:

        rotated_tile = cv2.rotate(
            tile,
            cv2.ROTATE_90_COUNTERCLOCKWISE
        )

    else:

        rotated_tile = tile.copy()

    return rotated_tile

# flip a tile

def flip_tile(
        self,
        tile,
        direction
):

    if direction == "horizontal":

        flipped_tile = cv2.flip(
            tile,
            1
        )

    elif direction == "vertical":

        flipped_tile = cv2.flip(
            tile,
            0
        )

    else:
        flipped_tile = tile.copy()

    return flipped_tile

# draw grind lines on the image

def draw_grid(
        self,
        image,
        grid_size

):

    image_with_grid = image.copy()

    height, weight = \
        image_with_grid.shape[0:2]

    tile_width =(
        height // grid_size
    )

# vertical grid lines
for column in range(
    1,
    grid_size
)

    x = column * tile_width

    cv2.line(
        image_with_grid,
        (x, 0),
        (x, height),
        (150, 150, 150),
        1
    )

# horizontal grind lines
for row in range(
    1,
    grid_size
):

    y = row * tile_height

    cv2. line(
        image_with_grid,
        (0, y),
        (width, y),
        (150, 150, 150),
        1
    )

return image_with_grid

# convert opencv bgr image to rgb because opencv uses bgr by default


def convert_to_rgb(
        self,
        image

):

    rgb_image = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB

    )
    return rgb_image