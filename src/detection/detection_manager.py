import gc
import threading
import time

import cv2
from datetime import datetime
from pathlib import Path
import logging

from ..stream.WebSocketStreamer import WebSocketStreamer
from ..utils.detection_utils import DetectionUtils
from ..utils.image_utils import ImageSave

"""
Kameradan alınan görüntüyü işleyen ve tespit yapan sınıf
"""
class DetectionManager:
    def __init__(self, all_settings, camera, detector, db_manager, save_dir="../data/camera"):

        self.camera = camera
        self.detector = detector
        self.db_manager = db_manager

        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)

        self.settings = all_settings

        self.last_detections = []
        self.last_save_time = datetime.now()
        self.frame_counter = 0
        self.gc_interval = 30
        self.processed_frame = None


        self.websocket_streamer = WebSocketStreamer(port=self.settings['wsPort'])
        self.ws_thread = threading.Thread(target=self.websocket_streamer.start_server)
        self.ws_thread.daemon = True
        self.ws_thread.start()

        time.sleep(1)

    def process_frame(self, frame):
        """Kareyi işler ve tespit yapar"""
        self.frame_counter += 1
        try:
            detections = self.detector.detect(frame)
            processed_frame, anomaly = DetectionUtils.draw_detections(frame.copy(), detections, self.settings)

            if self.frame_counter % self.gc_interval == 0:
                gc.collect()

            self.websocket_streamer.update_frame(processed_frame)

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
                        current_time=current_time
                    )

                except Exception as e:
                    logging.error(f"Görüntü kaydedilirken hata oluştu: {e}")
                    main_image_path = None

                if main_image_path:
                    detection_id = self.db_manager.db_save_detection(
                        source="camera",
                        source_name=self.camera.camera_id,
                        detections=detections,
                        image_path=main_image_path,
                        current_time = current_time,
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
                                    current_time = current_time
                                )

            return processed_frame
        finally:
            del frame

    def run(self):
        """Ana tespit döngüsünü çalıştırır"""
        try:
            frame_time = 1.0 / self.settings['fpsLimit']
            with self.camera:

                while True:
                    start_time = time.time()

                    frame = self.camera.read_frame()
                    if frame is None:
                        logging.warning("Kameradan görüntü alınamadı")
                        break

                    processed_frame = self.process_frame(frame)

                    elapsed_time = time.time() - start_time
                    if elapsed_time < frame_time:
                        time.sleep(frame_time - elapsed_time)

                    cv2.imshow('Object Detection', processed_frame)

                    key = cv2.waitKey(1) & 0xFF
                    if key == 27 or key == ord('q'):
                        break

        except Exception as e:
            logging.error(f"Tespit döngüsünde hata oluştu: {e}")
            raise

        finally:
            cv2.destroyAllWindows()
            del frame
            logging.info("Tespit sistemi kapatıldı")

    def __enter__(self):
        """Context başlangıcı"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context kapanışı"""
        if hasattr(self, 'websocket_streamer'):
            self.websocket_streamer.stop_server()

        if exc_type:
            logging.error(f"Hata ile kapatıldı: {exc_val}")
            return False
        return True