from django.conf import settings
from datetime import date
from pathlib import Path
import uuid
from PIL import Image
import pytesseract

def get_upload_directory():
    target_directory = settings.BASE_DIR / 'uploads' / date.today().strftime("%d-%m-%Y")

    Path(target_directory).mkdir(parents=True, exist_ok=True)

    return str(target_directory)

def handle_file_upload(file):
    upload_path = get_upload_directory()
    file_name = str(uuid.uuid4())
    extension = "." + file.content_type.split('/')[1]

    file_name = upload_path + "/" + file_name + extension

    with(open(file=file_name, mode="wb+") as target):
        for chunk in file.chunks():
            target.write(chunk)

    return file_name

def scrape_image_content(file_path):
    content = pytesseract.image_to_string(Image.open(file_path), lang='bul')

    if not content:
        return "No content found!"

    content = content.replace("\n", "<br>") 
    
    return content