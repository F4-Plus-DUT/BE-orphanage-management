import cloudinary
import cloudinary.api
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()


class ImageService:
    @classmethod
    def upload_image(cls, image, folder):
        upload_avatar = cloudinary.uploader.upload(image, folder=folder)
        return upload_avatar.get('url')
