from config.logger_config import logger
import requests
import os
from supabase import create_client, Client, StorageException
import hashlib
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv


class SupabaseStorageManager():
    def __init__(self):
        load_dotenv()
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        self.bucket_name = os.getenv("SUPABASE_BUCKET_NAME")
        self.supabase_client: Client = create_client(
            self.supabase_url, self.supabase_key)

    def upload_image(self, image_url, product_url):
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
        existing_files = bucket.list()

        if any(file['name'] == unique_filename for file in existing_files):
            logger.warn(
                f"A file with this name already exists: {unique_filename}")
            return f"{self.supabase_url}/storage/v1/object/public/{self.bucket_name}/{unique_filename}"

        try:
            bucket.upload(
                unique_filename, image_webp.getvalue(), file_options={"content-type": "image/webp"})
        except StorageException as e:
            error_message = str(e)
            if 'Duplicate' in error_message:
                logger.warn(
                    f"A file with this name already exists: {unique_filename} for {product_url}. Skipping upload.")
            else:
                logger.error(
                    f"Error uploading image for {product_url}: {error_message}")
        except Exception as e:
            logger.error(
                f"Unexpected error uploading image for {product_url}: {e}")

        logger.info("Image successfully uploaded!")
        return f"{self.supabase_url}/storage/v1/object/public/{self.bucket_name}/{unique_filename}"

    def delete_image(self, product_url):
        # Generate the unique filename based on the image URL
        hash_object = hashlib.md5(product_url.encode())
        unique_filename = hash_object.hexdigest() + ".webp"

        # Access the storage bucket
        storage = self.supabase_client.storage
        bucket = storage.StorageFileAPI(self.bucket_name)

        # Delete the image from the bucket
        delete_responses = bucket.remove([unique_filename])

        # Check if delete operation was successful
        if isinstance(delete_responses, list) and delete_responses:
            delete_response = delete_responses[0]
        else:
            logger.error(
                f"Unexpected response format from delete operation: {delete_responses}")
            return False
        if delete_response["metadata"]["httpStatusCode"] == 200:
            logger.info(f"Image successfully deleted: {unique_filename}")
            return True
        else:
            error_message = delete_response.get('error', {}).get('message', '')
            logger.error(
                f"Failed to delete image: {unique_filename}, {error_message}")
            return False
