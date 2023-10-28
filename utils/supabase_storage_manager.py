from config.logger_config import logger
import requests
import os
from supabase import create_client, Client
import hashlib
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv


class SupabaseStorageManager():
    def __init__(self):
        load_dotenv()
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_API_KEY")
        self.bucket_name = os.getenv("SUPABASE_BUCKET_NAME")
        self.supabase_client: Client = create_client(
            self.supabase_url, self.supabase_key)

    def get_storage_list(self):
        storage = self.supabase_client.storage
        bucket = storage.StorageFileAPI(self.bucket_name)
        return bucket.list()

    def upload_image(self, image_url, product_url, existing_files):
        # Generate a unique filename based on the image URL
        hash_object = hashlib.md5(product_url.encode())
        unique_filename = hash_object.hexdigest() + ".webp"

        # Download the image
        response = requests.get(image_url)
        if response.status_code != 200:
            logger.error(f"Failed to download image: {image_url}")
            return

        image = Image.open(BytesIO(response.content))

        # Resive the image
        aspect_ratio = image.width / image.height
        new_height = int(350 / aspect_ratio)
        image = image.resize((350, new_height))

        # Convert to WEBP
        image = image.convert("RGBA")
        image_webp = BytesIO()
        image.save(image_webp, "WEBP")

        # Upload to Supabase Storage
        storage = self.supabase_client.storage
        bucket = storage.StorageFileAPI(self.bucket_name)

        if any(file['name'] == unique_filename for file in existing_files):
            logger.error(
                f"A file with this name already exists: {unique_filename}")
            return f"{self.supabase_url}/storage/v1/object/public/{self.bucket_name}/{unique_filename}"

        upload_response = bucket.upload(
            unique_filename, image_webp.getvalue())

        if upload_response.status_code == 200:
            logger.info("Image successfully uploaded!")
            return f"{self.supabase_url}/storage/v1/object/public/{self.bucket_name}/{unique_filename}"
        else:
            logger.error("Failed to upload image:",
                         upload_response["error"]["message"])
            return None

    def delete_image(self, product_url):
        # Generate the unique filename based on the image URL
        hash_object = hashlib.md5(product_url.encode())
        unique_filename = hash_object.hexdigest() + ".webp"

        # Access the storage bucket
        storage = self.supabase_client.storage
        bucket = storage.StorageFileAPI(self.bucket_name)

        # Delete the image from the bucket
        delete_response = bucket.remove([unique_filename])

        if delete_response.status_code == 200:
            logger.info(f"Image successfully deleted: {unique_filename}")
            return True
        else:
            logger.error(
                f"Failed to delete image: {unique_filename}, {delete_response.get('error', {}).get('message', '')}")
            return False
