from pathlib import Path

from ultralytics import YOLO
import logging

"""
Görüntüden nesnelerin tespiti ve  kordinatlarını
"""
class ObjectDetector:
    def __init__(self, all_settings):

        # Doğruluk eşiği ve izin verilen sınıflar
        self.confidence_threshold = all_settings['confidenceThreshold']
        self.allowed_classes = set(all_settings['allowedClasses']) if all_settings['allowedClasses'] else None


        logging.getLogger("ultralytics").setLevel(logging.WARNING)

        model_dir = Path(__file__).parent.parent.parent / "models"
        model_path = model_dir / "yolov5su.pt"

        if not model_path.exists():
            raise FileNotFoundError(f"Model dosyası bulunamadı: {model_path}")

        try:
            self.model = YOLO(str(model_path), verbose=False)
        except Exception as e:
            print(f"Model yüklenirken hata oluştu: {e}")
            raise


    def detect(self, frame):
        """Görüntüdeki nesneleri tespit eder"""
        results = self.model(frame, conf=self.confidence_threshold, verbose=False)[0]
        detections = []

        for result in results.boxes.data:
            x1, y1, x2, y2, conf, cls = result
            x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
            class_id = int(cls)
            class_name = self.model.names[class_id]

            if self.allowed_classes is None or class_name in self.allowed_classes:
                detection = {
                    'bbox': (x1, y1, x2, y2),
                    'confidence': float(conf),
                    'class_name': class_name,
                    'class_id': class_id
                }
                detections.append(detection)

        return detections