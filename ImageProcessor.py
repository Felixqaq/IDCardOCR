from PIL import Image, ExifTags
import cv2
import numpy as np
import matplotlib.pyplot as plt

class ImageProcessor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = None

    def correct_image_orientation(self):
        with Image.open(self.image_path) as img:
            try:
                exif = img._getexif()
                if exif is not None:
                    for tag, value in exif.items():
                        if ExifTags.TAGS.get(tag) == 'Orientation':
                            orientation = value
                            break
                    else:
                        orientation = 1

                    if orientation == 3:
                        img = img.rotate(180, expand=True)
                    elif orientation == 6:
                        img = img.rotate(270, expand=True)
                    elif orientation == 8:
                        img = img.rotate(90, expand=True)
            except AttributeError:
                pass

            self.image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            cv2.imwrite(self.image_path, self.image)

    def preprocess_image(self, image_part, method='default'):
        gray = cv2.cvtColor(image_part, cv2.COLOR_BGR2GRAY)
        if method == 'default':
            _, binary = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
        elif method == 'adaptive':
            binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        binary = cv2.fastNlMeansDenoising(binary, None, 30, 7, 21)
        kernel = np.ones((2, 2), np.uint8)
        binary = cv2.dilate(binary, kernel, iterations=1)
        binary = cv2.erode(binary, kernel, iterations=1)
        self.show_image(binary)
        return binary

    def show_image(self, image):
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.axis('off')  # Hide axes
        plt.show()