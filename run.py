from config.settings import SettingsManager
from src.database.database_manager import DatabaseManager
from src.detection.camera import CameraManager
from src.detection.detection_manager import DetectionManager
from src.detection.detector import ObjectDetector

def main():
    db_manager = DatabaseManager()

    setting_manager = SettingsManager(db_manager=db_manager)
    all_settings = setting_manager.get_all_settings()

    camera_manager = CameraManager(all_settings=all_settings)
    detector = ObjectDetector(all_settings=all_settings)

    detection_manager = DetectionManager(
        all_settings=all_settings,
        camera=camera_manager,
        detector=detector,
        db_manager=db_manager,
        save_dir="data/camera"
    )

    try:
        detection_manager.run()
    except KeyboardInterrupt:
        print("Sonlandırılıyor...")


if __name__ == "__main__":
    main()