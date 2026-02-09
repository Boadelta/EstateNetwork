import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from dotenv import load_dotenv
import os

load_dotenv()
NAME = "dvfzxrlxc"
KEY = "448277556737947"
SECRET = "nj_3CiPhi-cU5XK_QtTeTrvCLEE"
def uploadImage(imageId, studId):
    cloudinary.config( 
    cloud_name = NAME, 
    api_key = KEY, 
    api_secret = SECRET, 
    secure=True)
    # Upload an image
    upload_result = cloudinary.uploader.upload(imageId,
                                           public_id=studId)
    
    # Optimize delivery by resizing and applying auto-format and auto-quality
    optimize_url, _ = cloudinary_url(studId, fetch_format="auto", quality="auto")
    # Transform the image: auto-crop to square aspect_ratio
    auto_crop_url, _ = cloudinary_url(studId, width=500, height=500, crop="auto", gravity="auto")
    return auto_crop_url
