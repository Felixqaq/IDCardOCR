import os
from paddleocr import PaddleOCR, draw_ocr
from ImageProcessor import ImageProcessor
from PIL import Image
from opencc import OpenCC

class ImageNotFoundException(Exception):
    pass

class IDCardOCR:
    def __init__(self, img_path='./pic/capture.jpg'):
        self._validate_image_path(img_path)
        self._initialize_paths(img_path)
        self._initialize_ocr()
        self._initialize_processor(img_path)
        self.address = []
        
    def _validate_image_path(self, img_path):
        if not os.path.exists(img_path):
            raise ImageNotFoundException(f"圖片未找到: {img_path}")
            
    def _initialize_paths(self, img_path):
        self.img_path = img_path
        self.font_path = "./font/simsun.ttc"
        
    def _initialize_ocr(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang="ch")
        
    def _initialize_processor(self, img_path):
        self.image_processor = ImageProcessor(img_path)

    def correct_orientation(self):
        self.image_processor.correct_image_orientation()

    def fetch_left_text(self, line, res):
        right_top = [line[0][1][0], line[0][1][1]-20]
        right_bottom = [line[0][2][0], line[0][2][1]+40]
        address = []
        for temp in res:
            if temp[0][0][0] > right_top[0] and temp[0][0][1] > right_top[1] and temp[0][0][1] < right_bottom[1]:
                address.append(temp)
        return address

    def list_to_str(self, list):
        result_str = ''
        for item in list:
            result_str += item[1][0]
        return result_str

    def sim_to_tra(self, text):
        cc = OpenCC('s2tw')
        return cc.convert(text)

    def process_image(self):
        self.correct_orientation()
        result = self._extract_ocr_result()
        self._extract_address(result)
        self._convert_address_format()
        self.draw_ocr_result(result[0])

    def _extract_ocr_result(self):
        return self.ocr.ocr(self.img_path, cls=True)

    def _extract_address(self, result):
        for res in result:
            for line in res:
                if line[1][0] == '住址':
                    self.address = self.fetch_left_text(line, res)
                    break

    def _convert_address_format(self):
        str_address = self.list_to_str(self.address)
        self.address = self.sim_to_tra(str_address)

    def draw_ocr_result(self, result):
        image = self._load_image()
        
        boxes, texts, scores = self._extract_ocr_data(result)
        
        output_image = self._draw_results(image, boxes, texts, scores)
        
        self._save_result_image(output_image)
    
    def _load_image(self):
        return Image.open(self.img_path).convert('RGB')
    
    def _extract_ocr_data(self, result):
        boxes = [line[0] for line in result]
        texts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        return boxes, texts, scores
    
    def _draw_results(self, image, boxes, texts, scores):
        drawn_image = draw_ocr(image, boxes, texts, scores, font_path=self.font_path)
        return Image.fromarray(drawn_image)
    
    def _save_result_image(self, image):
        image.save('./pic/result.jpg')

    def get_id_card_address(self):
        return self.address