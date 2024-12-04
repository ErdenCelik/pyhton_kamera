import json
from datetime import datetime

import cv2

from src.utils.object_translations import ObjectTranslations


class DetectionUtils:
    @staticmethod
    def box_area(box):
        """Alan hesaplar"""
        x1, y1, x2, y2 = box
        return (x2 - x1) * (y2 - y1)

    @staticmethod
    def intersection_rate(box1, box2):
        """İki kutu arasındaki kesisme değerini hesaplar"""
        x1_1, y1_1, x2_1, y2_1 = box1
        x1_2, y1_2, x2_2, y2_2 = box2

        x_min = max(x1_1, x1_2)
        y_min = max(y1_1, y1_2)
        x_max = min(x2_1, x2_2)
        y_max = min(y2_1, y2_2)

        if x_max < x_min or y_max < y_min:
            return 0.0

        intersection_area= (x_max - x_min) * (y_max - y_min)
        box1_area = (x2_1 - x1_1) * (y2_1 - y1_1)
        box2_area = (x2_2 - x1_2) * (y2_2 - y1_2)
        total_area = box1_area + box2_area - intersection_area

        if total_area == 0:
            return 0.0

        return intersection_area / total_area

    @staticmethod
    def is_detection_changes(last_detections, new_detections, settings):
        """Yeni tespitler öncekilerden farklı mı kontrol eder"""
        if not last_detections and not new_detections:
            return False

        if len(last_detections) != len(new_detections):
            return True

        for old_det in last_detections:
            found_match = False
            old_box = old_det['bbox']
            old_class = old_det['class_name']
            old_area = DetectionUtils.box_area(old_box)

            for new_det in new_detections:
                new_box = new_det['bbox']
                new_class = new_det['class_name']
                new_area = DetectionUtils.box_area(new_box)

                if old_class == new_class:
                    area_diff = abs(old_area - new_area) / max(old_area, new_area)
                    if area_diff < settings.get('minAreaDifference', 0.3):
                        intersection_rate = DetectionUtils.intersection_rate(old_box, new_box)
                        if intersection_rate > settings.get('minIou', 0.7):
                            found_match = True
                            break

            if not found_match:
                return True

        return False

    @staticmethod
    def is_frame_save(settings, last_detections, last_save_time, frame_counter, new_detections):
        """
        Tespitlerin kaydedilip kaydedilmeyeceğini kontrol eder
        """
        if frame_counter % settings['skipFrames'] != 0:
            return False

        current_time = datetime.now()
        time_diff = (current_time - last_save_time).total_seconds()
        if time_diff < settings['minSaveInterval']:
            return False

        return DetectionUtils.is_detection_changes(
            last_detections,
            new_detections,
            settings
        )

    @staticmethod
    def is_anomaly(frame, detections, threshold=0.1):
        """Nesne yogunlugu tespiti yapar"""
        height, width = frame.shape[:2]
        total_area = height * width

        detection_areas = []
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            area = (x2 - x1) * (y2 - y1)
            detection_areas.append(area)

        total_detection_area = sum(detection_areas)
        density = total_detection_area / total_area

        if density > threshold:
            return True, density
        return False, density

    @staticmethod
    def draw_detections(frame, detections, settings):
        """Tespit edilen nesneleri çiz"""

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        thickness = 1

        is_anomaly, density = DetectionUtils.is_anomaly(frame, detections,
                                                                                settings['densityThreshold'])
        if is_anomaly:
            height, width = frame.shape[:2]

            density_text = f"Yogunluk: {density:.2f}"

            (text_width, text_height), _ = cv2.getTextSize(density_text, font, font_scale, thickness)

            text_x = 10
            text_y = height - 10

            cv2.rectangle(frame,
                          (text_x - 5, text_y + 5),
                          (text_x + text_width + 5, text_y - text_height - 5),
                          (0, 0, 0),
                          -1)
            cv2.putText(frame, density_text, (text_x, text_y),
                        font, font_scale, (0, 0, 255), thickness)

        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            turkish_name = ObjectTranslations.translate(det['class_name'])

            label = f"{turkish_name} - {det['confidence']:.2f}"

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            label_size = cv2.getTextSize(label, font, font_scale, thickness)[0]
            cv2.rectangle(frame,
                          (x1, y1 - 25),
                          (x1 + label_size[0], y1),
                          (0, 0, 0),
                          -1)

            cv2.putText(frame, label, (x1, y1 - 5),
                        font, font_scale, (255, 255, 255), thickness)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        height, width = frame.shape[:2]

        (text_width, text_height), _ = cv2.getTextSize(timestamp, font, font_scale, thickness)

        text_x = width - text_width - 10
        text_y = height - 10

        cv2.rectangle(frame,
                      (text_x - 5, text_y + 5),
                      (text_x + text_width + 5, text_y - text_height - 5),
                      (0, 0, 0),
                      -1)

        cv2.putText(frame, timestamp, (text_x, text_y),
                    font, font_scale, (255, 255, 255), thickness)

        return frame,is_anomaly

    @staticmethod
    def detection_db_save(db_manager, source, source_name, detections, image_path):
        class_names = [det['class_name'] for det in detections]
        class_names_json = json.dumps(class_names, ensure_ascii=False)
        try:
            return db_manager.save_detection(
                source=source,
                source_name=source_name,
                object_count=len(detections),
                detected_objects=class_names_json,
                image_path=image_path
            )
        except Exception as e:
            pass