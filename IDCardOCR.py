from paddleocr import PaddleOCR, draw_ocr
from ImageProcessor import ImageProcessor
from PIL import Image
from opencc import OpenCC

class IDCardOCR:
    def __init__(self, img_path, font_path):
        self.img_path = img_path
        self.font_path = font_path
        self.ocr = PaddleOCR(use_angle_cls=True, lang="ch")
        self.image_processor = ImageProcessor(img_path)
        self.address = []

    def correct_orientation(self):
        self.image_processor.correct_image_orientation()

    def fetch_left_text(self, line, res):
        right_top = [line[0][1][0]+5, line[0][1][1]-20]
        right_bottom = [line[0][2][0]+5, line[0][2][1]+50]
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
        result = self.ocr.ocr(self.img_path, cls=True)
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                if line[1][0] == '住址':
                    self.address = self.fetch_left_text(line, res)
        str_address = self.list_to_str(self.address)
        self.address = self.sim_to_tra(str_address)
        self.draw_ocr_result(result[0])

    def draw_ocr_result(self, result):
        image = Image.open(self.img_path).convert('RGB')
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        im_show = draw_ocr(image, boxes, txts, scores, font_path=self.font_path)
        im_show = Image.fromarray(im_show)
        im_show.save('result.jpg')

# 使用範例
img_path = '.\pic\IDback.jpg'
font_path = ".\font\simsun.ttc"
id_card_ocr = IDCardOCR(img_path, font_path)
id_card_ocr.process_image()
print(id_card_ocr.address)