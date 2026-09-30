import cv2

class ImageProcessor:

    def __init__(self, max_width=600, max_height=600):
        self.max_width = max_width
        self.max_height = max_height


# load image from file

def load_image(self, file_path):

    image = cv2.imread(file_path)

    if image is None:
        raise ValueError("Image could not be loaded. Please check the file path.")

    return image



# Resize image with aspect ratio preserved

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