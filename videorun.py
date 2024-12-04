import warnings
import sys
import logging
import argparse

from config.settings import SettingsManager
from src.detection.detector import ObjectDetector
from src.database.database_manager import DatabaseManager
from src.detection.video_analyzer import VideoAnalyzer

warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)

def main():
    parser = argparse.ArgumentParser(description='Video Analiz Sistemi')
    parser.add_argument('video_path', help='Analiz edilecek video dosyasının yolu')
    parser.add_argument('--no-output', '-o', action='store_true', help='İşlenmiş videoyu kaydetmeyi devre dışı bırak')
    parser.add_argument('--no-preview', '-np', action='store_true', help='Önizleme penceresini devre dışı bırak')

    args = parser.parse_args()

    db_manager = DatabaseManager()
    setting_manager = SettingsManager(db_manager=db_manager)
    all_settings = setting_manager.get_all_settings()


    try:
        detector = ObjectDetector(all_settings=all_settings)
        db_manager = DatabaseManager()

        analyzer = VideoAnalyzer(
            all_settings=all_settings,
            detector=detector,
            db_manager=db_manager,
            save_dir="data/video",
            video_path = args.video_path,
            output=not args.no_output,
            show_preview=not args.no_preview
        )

        analyzer.analyze_video()

    except Exception as e:
        logging.error(f"Hata oluştu: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()