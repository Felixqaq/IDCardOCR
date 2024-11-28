import os
from paddleocr import PaddleOCR, draw_ocr
from ImageProcessor import ImageProcessor
from PIL import Image
from opencc import OpenCC
from Logger import Logger

class ImageNotFoundException(Exception):
    pass

class IDCardOCR:
    # 定義常量
    ADDRESS_PADDING = {
        'TOP': 20,
        'BOTTOM': 40
    }
    DEFAULT_OUTPUT_PATH = './pic/result.jpg'
    
    def __init__(self, img_path='./pic/capture.jpg', font_path="./font/simsun.ttc"):
        self.logger = Logger()
        self._validate_image_path(img_path)
        self._validate_image_path(font_path)
        self._initialize_paths(img_path, font_path)
        self._initialize_ocr()
        self._initialize_processor(img_path)
        self.address = []
        
    def _validate_image_path(self, img_path):
        if not os.path.exists(img_path):
            raise ImageNotFoundException(f"圖片未找到: {img_path}")
            
    def _initialize_paths(self, img_path, font_path):
        self.img_path = img_path
        self.font_path = font_path
        
    def _initialize_ocr(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang="ch")
        
    def _initialize_processor(self, img_path):
        self.image_processor = ImageProcessor(img_path)

    def correct_orientation(self):
        self.image_processor.correct_image_orientation()

    def extract_address_region(self, reference_line, result_lines):
        right_top = [
            reference_line[0][1][0],
            reference_line[0][1][1] - self.ADDRESS_PADDING['TOP']
        ]
        right_bottom = [
            reference_line[0][2][0],
            reference_line[0][2][1] + self.ADDRESS_PADDING['BOTTOM']
        ]
        
        return [
            line for line in result_lines
            if self._is_within_address_region(line, right_top, right_bottom)
        ]

    def _is_within_address_region(self, line, top, bottom):
        return (line[0][0][0] > top[0] and 
                line[0][0][1] > top[1] and 
                line[0][0][1] < bottom[1])

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
        self._validate_ocr_result(result)
        self._find_and_extract_address(result)
        self._check_address_extraction()

    def _validate_ocr_result(self, result):
        if result == [None]:
            error_msg = "OCR結果為空"
            raise ImageNotFoundException(error_msg)

    def _find_and_extract_address(self, result):
        for res in result:
            for line in res:
                if line[1][0] == '住址':
                    self.address = self.extract_address_region(line, res)
                    self.logger.info("成功提取地址欄位")
                    return

    def _check_address_extraction(self):
        if self.address == []:
            error_msg = "未找到住址"
            raise ImageNotFoundException(error_msg)

    def _convert_address_format(self):
        str_address = self.list_to_str(self.address)
        self.address = self.sim_to_tra(str_address)

    def draw_ocr_result(self, result):
        image = self._load_image()
        
        boxes, texts, scores = self._extract_ocr_data(result)
        
        output_image = self._draw_results(image, boxes, texts, scores)
        
        self._save_result_image(output_image)
    
    def _load_image(self):
        try:
            return Image.open(self.img_path).convert('RGB')
        except Exception as e:
            raise ImageNotFoundException(f"無法載入圖片: {str(e)}")
    
    def _extract_ocr_data(self, result):
        boxes = [line[0] for line in result]
        texts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        return boxes, texts, scores
    
    def _draw_results(self, image, boxes, texts, scores):
        drawn_image = draw_ocr(image, boxes, texts, scores, font_path=self.font_path)
        return Image.fromarray(drawn_image)
    
    def _save_result_image(self, image, output_path=None):
        try:
            output_path = output_path or self.DEFAULT_OUTPUT_PATH
            image.save(output_path)
        except Exception as e:
            raise Exception(f"保存結果圖片失敗: {str(e)}")

    def get_id_card_address(self):
        return self.address