import pytesseract
from ImageProcessor import ImageProcessor

class TextExtractor:
    def __init__(self, image):
        self.image = image
        self.text = ""

    def extract_text(self, method='default'):
        height, width = self.image.shape[:2]
        upper_half = self.image[:height//2, :]
        lower_half = self.image[height//2:, :]

        upper_text = self.extract_text_from_image_part(upper_half, method)
        lower_text = self.extract_text_from_image_part(lower_half, method)

        self.text = upper_text + "\n" + lower_text
        print(f"Extracted Text with method {method}:", self.text)

        return self.text

    def extract_text_from_image_part(self, image_part, method):
        processor = ImageProcessor(None)
        binary = processor.preprocess_image(image_part, method)
        text = pytesseract.image_to_string(binary, lang='chi_tra')
        return text