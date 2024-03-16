import os
import secrets
from PIL import Image

from flask import current_app
from wtforms.validators import ValidationError

from application import login_manager
from application.models import User

# FORM UTILS

def exists_email(form, field):
    user = User.query.filter_by(email=field.data).first()
    if user:
        raise ValidationError("Email already exists. Please use a different email.")
    
def not_exists_email(form, field):
    user = User.query.filter_by(email=field.data).first()
    if not user:
        raise ValidationError("Email not found.")

def exists_username(form, field):
    user = User.query.filter_by(username=field.data).first()
    if user:
        raise ValidationError("Username already exists. Please use a different username.")

# END OF FORM UTILS

# LOGIN MANAGER UTILS

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# END OF LOGIN MANAGER UTILS

def save_image(form_picture_data, folder='posts'):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture_data.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/images', folder, picture_filename)

    output_size = (125, 125)
    image = Image.open(form_picture_data)
    image.thumbnail(output_size)
    
    image.save(picture_path)

    return os.path.join('images', folder, picture_filename)

# def delete_image(image_path):
#     full_path = os.path.join(current_app.root_path, 'static', image_path)
#     if os.path.exists(full_path):
#         os.remove(full_path)
#         return True
#     return False
