import os
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    print(value)
    ext = os.path.splitext(value.name)[1]
    valid_extentions = ['.mp4','.avi','.mpeg','.mov','.webm','.mp3','.wav']
    if not ext.lower() in valid_extentions:
        raise ValidationError('Unsupported file extension :(')
