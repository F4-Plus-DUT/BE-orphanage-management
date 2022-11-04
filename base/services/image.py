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

    @classmethod
    def upload_list_image(cls, images, folder):
        rs = []
        for image in images:
            link = cloudinary.uploader.upload(image, folder=folder).get('url')
            rs.append(link)
        return rs
