import logging
import cv2

class ImageSave:
    @staticmethod
    def save_detection_image(save_dir, frame, current_time):
        """Tespit görüntüsünü kaydeder"""
        try:
            year = current_time.strftime('%Y')
            month = current_time.strftime('%m')
            day = current_time.strftime('%d')
            hour = current_time.strftime('%H')

            save_path = save_dir / year / month / day / hour
            save_path.mkdir(parents=True, exist_ok=True)

            filename = f"{current_time.strftime('%Y%m%d_%H%M%S_%f')}.jpg"
            save_path = save_path / filename

            cv2.imwrite(str(save_path), frame)
            return str(save_path)

        except Exception as e:
            logging.error(f"Görüntü kaydedilirken hata oluştu: {e}")
            return None

    @staticmethod
    def save_detection_object_image(save_dir, frame, current_time, detection):
        """Tespit edilen nesnenin görüntüsünü kaydeder"""
        try:
            year = current_time.strftime('%Y')
            month = current_time.strftime('%m')
            day = current_time.strftime('%d')
            hour = current_time.strftime('%H')

            save_path = save_dir / year / month / day / hour
            save_path.mkdir(parents=True, exist_ok=True)

            x1, y1, x2, y2 = detection['bbox']
            padding = 20
            x1 = max(0, x1 - padding)
            y1 = max(0, y1 - padding)
            x2 = min(frame.shape[1], x2 + padding)
            y2 = min(frame.shape[0], y2 + padding)

            cropped_frame = frame[y1:y2, x1:x2]

            filename = f"{detection['class_name']}_{current_time.strftime('%M%S_%f')}.jpg"
            save_path = save_path / filename

            cv2.imwrite(str(save_path), cropped_frame)
            return str(save_path)

        except Exception as e:
            logging.error(f"Görüntü kaydedilirken hata oluştu: {e}")
            return None