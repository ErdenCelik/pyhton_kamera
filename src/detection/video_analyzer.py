import cv2
from datetime import datetime
from pathlib import Path
import logging
from ..utils.detection_utils import DetectionUtils
from ..utils.image_utils import ImageSave

"""
Kameradan alınan görüntüyü işleyen ve tespit yapan sınıf
"""
class VideoAnalyzer:
    def __init__(self, all_settings, detector, db_manager, video_path, save_dir="../data/video", output=False, show_preview=True):

        self.detector = detector
        self.db_manager = db_manager

        self.video_path = Path(video_path)
        self.output = output
        self.show_preview = show_preview
        video_name = self.video_path.name

        base_save_dir = Path(save_dir) / f"{video_name}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

        self.save_dir = Path(base_save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)

        self.settings = all_settings

        self.last_detections = []
        self.last_save_time = datetime.now()
        self.frame_counter = 0




    def analyze_video(self):
        """
        video dosyasını okur ve nesne tespiti yapar
        """

        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise ValueError(f"Video dosyası açılamadı: {self.video_path}")

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        if self.output:
            output_path = self.save_dir / f"output.mp4"

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        else:
            out = None

        try:
            frame_count = 0

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                frame_count += 1
                self.frame_counter += 1

                detections = self.detector.detect(frame)
                processed_frame, anomaly = DetectionUtils.draw_detections(frame.copy(), detections, self.settings)

                should_save = DetectionUtils.is_frame_save(
                    settings=self.settings,
                    last_detections=self.last_detections,
                    last_save_time=self.last_save_time,
                    frame_counter=self.frame_counter,
                    new_detections=detections
                )

                if detections and should_save:
                    current_time = datetime.now()

                    try:
                        main_image_path = ImageSave.save_detection_image(
                            save_dir=self.save_dir,
                            frame=processed_frame,
                            current_time=current_time,
                        )
                    except Exception as e:
                        logging.error(f"Görüntü kaydedilirken hata oluştu: {e}")
                        main_image_path = None

                    if main_image_path:
                        detection_id = self.db_manager.db_save_detection(
                            source="video",
                            source_name=self.video_path.name,
                            detections=detections,
                            image_path=main_image_path,
                            current_time=current_time,
                            is_anomaly=anomaly
                        )
                        if detection_id:
                            self.last_save_time = current_time
                            self.last_detections = detections
                            for det in detections:
                                try:
                                    object_image_path = ImageSave.save_detection_object_image(
                                        save_dir=self.save_dir,
                                        frame=processed_frame,
                                        current_time=current_time,
                                        detection=det
                                    )
                                except Exception as e:
                                    logging.error(f"Tespit kaydedilirken hata oluştu: {e}")
                                    object_image_path = None

                                if object_image_path:
                                    self.db_manager.db_save_detection_object(
                                        detection_id=detection_id,
                                        object_type=det['class_name'],
                                        confidence=det['confidence'],
                                        image_path=object_image_path,
                                        current_time=current_time
                                    )

                if out:
                    out.write(processed_frame)

                if self.show_preview:
                    cv2.imshow('Object Detection', processed_frame)

                    key = cv2.waitKey(1) & 0xFF
                    if key == 27 or key == ord('q'):
                        break

        except Exception as e:
            logging.error(f"Video analizi sırasında hata oluştu: {e}")
            raise

        finally:
            # Kaynakları temizle
            cap.release()
            if out:
                out.release()
            cv2.destroyAllWindows()


    def __enter__(self):
        """Context manager başlangıcı"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager bitişi"""
        if exc_type:
            logging.error(f"Hata ile kapatıldı: {exc_val}")
            return False
        return True