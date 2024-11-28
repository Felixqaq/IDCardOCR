import os
from Camera import Camera
from Logger import Logger

class IDCardProcessor:
    def __init__(self):
        self.camera = Camera(save_to_file=True)
        self.ocr = None
        self.address = None
        self.logger = Logger()

    def capture_and_process(self):
        self.camera.open_camera()
        self.logger.info("照片拍攝完成")

        from IDCardOCR import IDCardOCR
        self.ocr = IDCardOCR(img_path='./pic/capture.jpg')
        self.ocr.process_image()
        self.address = self.ocr.get_id_card_address()
        self.logger.info(f"地址辨識完成: {self.address}")

    def get_address(self):
        return self.address

if __name__ == "__main__":
    processor = IDCardProcessor()
    try:
        processor.capture_and_process()
        print(f"識別出的地址: {processor.get_address()}")
    except Exception as e:
        processor.logger.error(f"處理過程發生錯誤: {str(e)}")