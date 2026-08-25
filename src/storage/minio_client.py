import os
from minio import Minio
from dotenv import load_dotenv
from io import BytesIO
import json

load_dotenv()


class MinIOClient:

    
    def __init__(self,bucket_name:str=None):
        
        endpoint = os.getenv("MINIO_ENDPOINT")
        access = os.getenv("MINIO_ROOT_USER")
        secret = os.getenv("MINIO_ROOT_PASSWORD")
        if not all([endpoint ,access,secret]):
            raise ValueError("Thiếu cấu hình trong .env")

        self.client = Minio (
            endpoint,
            access_key=access,
            secret_key=secret,
            secure=False
        )
        self.bucket_name = bucket_name or os.getenv("MINIO_BUCKET_NAME", "football-data")
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
            
        except Exception as e:
            print("Error!!!")
            raise
            

    
    def upload_json(self, data: dict|list, object_name:str):
        try:
            json_str= json.dumps(data,ensure_ascii=False,indent=4)
            json_bytes=json_str.encode("utf-8")
        
            buffer = BytesIO(json_bytes)
            
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                data=buffer,
                length=len(json_bytes),
                content_type="application/json",
            )
            return object_name
        
        except Exception as e:
            print(f"❌ Lỗi khi upload JSON từ RAM: {e}")
            raise
    
    def download_json(self,object_name: str) -> dict|list:
        response = None
        try:
            response = self.client.get_object(
                bucket_name=self.bucket_name,
                object_name=object_name)
        
            data_bytes=response.read()
            data = json.loads(data_bytes.decode("utf-8"))
            
            return data
        
        except Exception as e:
            print(f"❌ Lỗi khi đọc JSON từ MinIO: {e}")
            raise
        finally:
            if response:
                response.close()
                response.release_conn()
        