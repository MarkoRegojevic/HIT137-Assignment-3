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

