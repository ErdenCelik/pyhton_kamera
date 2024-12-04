from pathlib import Path
import json


class SettingsManager:
    def __init__(self, db_manager):
        self.BASE_DIR = Path(__file__).parent.parent
        self.LOG_DIR = self.BASE_DIR / 'logs'

        self.db_manager = db_manager

    def _convert_value(self, value_str, value_type):
        """String değerini belirtilen tipte değere dönüştürür"""
        if value_str is None:
            return None

        if value_type == 'float':
            return float(value_str)
        elif value_type == 'int':
            return int(value_str)
        elif value_type == 'bool':
            return value_str == 'true'
        elif value_type == 'json':
            return json.loads(value_str) if value_str else None
        return value_str

    def get_all_settings(self):
        """Tüm ayarları getir"""
        settings = {
            'LOG_DIR': str(self.LOG_DIR)
        }

        setting = self.db_manager.db_get_all_settings()
        for key, value, value_type in setting:
            settings[key] = self._convert_value(value, value_type)

        return settings