import re
from ImageProcessor import ImageProcessor
from TextExtractor import TextExtractor

class IDCardProcessor:
    def __init__(self, image_path):
        self.image_processor = ImageProcessor(image_path)
        self.text_extractor = None
        self.address = ""
        self.parents = ""
        self.birthplace = ""

    def process_image(self):
        self.image_processor.correct_image_orientation()
        self.text_extractor = TextExtractor(self.image_processor.image)
        methods = ['default', 'adaptive']
        for method in methods:
            text = self.text_extractor.extract_text(method)
            self.extract_address()
            self.extract_parents()
            self.extract_birthplace()
            if self.address:
                break
        self.extract_address()
        self.extract_parents()
        self.extract_birthplace()
        self.image_processor.show_image(self.image_processor.image)

    def extract_address(self):
        address_pattern = re.compile(r'住\s*址[:：]?\s*(.*(?:\n.*)?)')
        address_match = address_pattern.search(self.text_extractor.text)
        if address_match:
            self.address = address_match.group(1).replace('\n', '').replace(' ', '')
            print("Extracted Address:", self.address)
        else:
            print("Address not found")

    def extract_parents(self):
        parents_pattern = re.compile(r'父\s*母[:：]?\s*(.*(?:\n.*)?)')
        parents_match = parents_pattern.search(self.text_extractor.text)
        if parents_match:
            self.parents = parents_match.group(1).replace('\n', '').replace(' ', '')
            print("Extracted Parents:", self.parents)
        else:
            print("Parents not found")

    def extract_birthplace(self):
        birthplace_pattern = re.compile(r'出\s*生\s*地[:：]?\s*(.*(?:\n.*)?)')
        birthplace_match = birthplace_pattern.search(self.text_extractor.text)
        if birthplace_match:
            self.birthplace = birthplace_match.group(1).replace('\n', '').replace(' ', '')
            print("Extracted Birthplace:", self.birthplace)
        else:
            print("Birthplace not found")