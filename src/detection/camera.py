import cv2
import logging
import platform

class CameraManager:
    def __init__(self, all_settings):
        self.camera_id = 0
        self.width = all_settings['frameWidth']
        self.height = all_settings['frameHeight']
        self.cap = None
        self.system = platform.system()

    def start(self):
        """Kamerayı başlatır"""
        try:
            if self.system == "Darwin":
                camera_options = [
                    self.camera_id,
                    cv2.CAP_AVFOUNDATION + self.camera_id
                ]
                for option in camera_options:
                    self.cap = cv2.VideoCapture(option)
                    if self.cap is not None and self.cap.isOpened():
                        break
            else:
                self.cap = cv2.VideoCapture(self.camera_id, cv2.CAP_DSHOW if self.system == "Windows" else cv2.CAP_ANY)

            if self.cap is None or not self.cap.isOpened():
                raise Exception(f"Kamera {self.camera_id} açılamadı!")

            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

            if self.system == "Windows":
                self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

            logging.info(f"Kamera başarıyla başlatıldı: {self.camera_id}")
            return True

        except Exception as e:
            logging.error(f"Kamera başlatılırken hata oluştu: {e}")
            if self.cap:
                self.cap.release()
            raise

    def stop(self):
        """Kamerayı durdurur"""
        if self.cap and self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()

    def read_frame(self):
        """Kameradan görüntü oku"""
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return frame
            else:
                logging.warning("Kameradan görntü okunamadı")
        return None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()