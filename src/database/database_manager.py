import uuid

import mysql.connector
import json
from config.database import DatabaseConfig


class DatabaseManager:
    def __init__(self):
        self.config = DatabaseConfig.get_config()

    def connect(self):
        """Veritabanı bağlantısı oluşturur"""
        try:
            connection = mysql.connector.connect(**self.config)
            return connection
        except mysql.connector.Error as err:
            print(f"Veritabanı bağlantı hatası: {err}")
            raise

    def db_get_all_settings(self):
        """Tüm ayarları getir"""
        try:
            connection = self.connect()
            cursor = connection.cursor()

            cursor.execute("""SELECT setting_key, setting_value, setting_type FROM system_settings""")
            settings = cursor.fetchall()

            cursor.close()
            connection.close()

            return settings

        except mysql.connector.Error as err:
            print(f"Ayar getirme hatası: {err}")
            raise
        
    def db_save_detection(self, source, source_name, detections, image_path, current_time, is_anomaly=False):
        """Tespit edilen nesneyi veritabanına kaydeder"""
        try:
            connection = self.connect()
            cursor = connection.cursor()

            class_names = [det['class_name'] for det in detections]
            class_names_json = json.dumps(class_names, ensure_ascii=False)

            sql = """INSERT INTO detections 
                    (uuid, source, source_name, object_count, detected_objects, is_anomaly, image_path, created_at) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

            values = (str(uuid.uuid1()), source, source_name, len(class_names), class_names_json, is_anomaly, image_path, current_time)

            cursor.execute(sql, values)
            connection.commit()

            detection_id = cursor.lastrowid

            cursor.close()
            connection.close()

            return detection_id

        except mysql.connector.Error as err:
            print(f"Tespit kaydetme hatası: {err}")
            raise

    def db_save_detection_object(self, detection_id, object_type, confidence, image_path, current_time):
        """Tespit edilen nesneyi veritabanına kaydeder"""
        try:
            connection = self.connect()
            cursor = connection.cursor()

            sql = """INSERT INTO detection_objects 
                    (uuid, detection_id, object_type, confidence, image_path, created_at) 
                    VALUES (%s, %s, %s, %s, %s, %s)"""

            values = (str(uuid.uuid1()), detection_id, object_type, confidence, image_path, current_time)

            cursor.execute(sql, values)
            connection.commit()

            detection_id = cursor.lastrowid

            cursor.close()
            connection.close()

            return detection_id

        except mysql.connector.Error as err:
            print(f"Tespit kaydetme hatası: {err}")
            raise

    def db_get_detection_path(self, uuid_key):
        """Tespit edilen nesneyi veritabanından getirir"""
        try:
            connection = self.connect()
            cursor = connection.cursor()

            sql = """SELECT image_path FROM detections WHERE uuid = %s"""

            cursor.execute(sql, (uuid_key,))
            result = cursor.fetchone()

            cursor.close()
            connection.close()

            return result[0] if result else None

        except mysql.connector.Error as err:
            print(f"Tespit getirme hatası: {err}")
            raise

    def db_get_detection_object_path(self, uuid_key):
        """Tespit edilen nesneyi veritabanından getirir"""
        try:
            connection = self.connect()
            cursor = connection.cursor()

            sql = """SELECT image_path FROM detection_objects WHERE uuid = %s"""

            cursor.execute(sql, (uuid_key,))
            result = cursor.fetchone()

            cursor.close()
            connection.close()

            return result[0] if result else None

        except mysql.connector.Error as err:
            print(f"Tespit getirme hatası: {err}")
            raise

