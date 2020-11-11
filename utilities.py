import os
from flask import render_template, request, redirect, url_for,send_file
from  werkzeug.utils import secure_filename
import random
import string
#Vianney

def get_random_alphanumeric_string(letters_count, digits_count):
    sample_str = ''.join((random.choice(string.ascii_uppercase) for i in range(letters_count)))
    sample_str += ''.join((random.choice(string.digits) for i in range(digits_count)))

    # Convert string to list and shuffle it to mix letters and digits
    sample_list = list(sample_str)
    random.shuffle(sample_list)
    final_string = ''.join(sample_list)
    return final_string


#Create a directory in a known location to save files to . 
uploads_dir = "app/static/uploads/"
# uploads_dir = "app/static/uploads/" 
os.makedirs(uploads_dir, exist_ok=True)

def file_upload(method,files_data,name,nb='one'):
    if method == 'POST' and files_data.files:
        # save the single "profile" file
        print(files_data.files[name].filename)
        if (nb=='one') and files_data.files[name].filename:
            print(files_data.files)
            data = files_data.files[name]
            filename = secure_filename(data.filename)
            data.save(os.path.join(uploads_dir, filename))
            return filename

        if (nb=='*') and files_data.files[name].filename:
            filename = []
            for file in files_data.files.getlist(name):
                filename.append(secure_filename(data.filename))
                file.save(os.path.join(uploads_dir, filename[-1]))
            return filename

    return False


def dowloadFile():
    path = os.path.join(uploads_dir,"carte_grise.jpg")
    return send_file(path, as_attachment=True)