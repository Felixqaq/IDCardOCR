import cv2

class Camera:
    def __init__(self, save_to_file=False):
        self.cap = None
        self.captured_frame = None
        self.save_to_file = save_to_file

    def open_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.show_frame()

    def show_frame(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            frame = self.add_text_to_frame(frame, "Press 'Enter' to Capture")

            cv2.imshow("Camera", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == 13:  # Enter 鍵的 ASCII 碼是 13
                self.capture()
                break
            elif key == ord('q'):
                break

        self.on_closing()

    def add_text_to_frame(self, frame, text):
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_color = (0, 255, 0)
        thickness = 2
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_x = (frame.shape[1] - text_size[0]) // 2
        text_y = 30
        cv2.putText(frame, text, (text_x, text_y), font, font_scale, font_color, thickness, cv2.LINE_AA)
        return frame

    def capture(self):
        ret, frame = self.cap.read()
        if ret:
            self.captured_frame = frame
            if self.save_to_file:
                file_path = "./pic/capture.jpg"
                cv2.imwrite(file_path, frame)
                print(f"Image saved to {file_path}")

    def show_captured_frame(self):
        if self.captured_frame is not None:
            cv2.imshow("Captured Frame", self.captured_frame)
            while True:
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cv2.destroyWindow("Captured Frame")
        else:
            print("No frame captured yet.")

    def on_closing(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def getResult(self):
        return self.captured_frame