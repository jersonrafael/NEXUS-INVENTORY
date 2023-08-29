import cloudinary
# Import the cloudinary.api for managing assets
import cloudinary.api
# Import the cloudinary.uploader for uploading assets
import cloudinary.uploader

import os
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name= os.getenv('cloud_name'),
    api_key= os.getenv('api_key'),
    api_secret= os.getenv('api_secret'),
    secure= os.getenv('secure'),
)

