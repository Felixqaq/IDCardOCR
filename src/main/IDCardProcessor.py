import os
from Camera import Camera

class IDCardProcessor:
    def __init__(self):
        self.camera = Camera(save_to_file=True)
        self.ocr = None
        self.address = None

    def capture_and_process(self):
        self.camera.open_camera()

        from IDCardOCR import IDCardOCR
        self.ocr = IDCardOCR(img_path='./pic/2.jpg')
        self.ocr.process_image()
        self.address = self.ocr.get_id_card_address()

    def get_address(self):
        return self.address

if __name__ == "__main__":
    processor = IDCardProcessor()
    try:
        processor.capture_and_process()
        print(f"識別出的地址: {processor.get_address()}")
    except Exception as e:
        print(e)