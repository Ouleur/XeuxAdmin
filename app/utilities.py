import os
from flask import render_template, request, redirect, url_for,send_file,current_app
from  werkzeug.utils import secure_filename
import random
import string
from datetime import timedelta

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
def get_path(app,uploads_dir):
    with app.get_context():
        os.makedirs(uploads_dir, exist_ok=True)
        return uploads_dir



def file_upload(method,files_data,name,nb='one'):
    app = current_app._get_current_object()

    uploads_dir = app.config['UPLOADS_DIR']

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
    app = current_app._get_current_object()

    uploads_dir = app.config['UPLOADS_DIR']
    
    path = os.path.join(uploads_dir,"carte_grise.jpg")
    return send_file(path, as_attachment=True)


def time_Average(tickets):
    e = 0
    allTickets = tickets.all()
    time = timedelta(days=365) - timedelta(days=365)
    for ticket in allTickets:

        if e > 0 and ticket.date_modify:
            time += ticket.date_modify-allTickets[e-1].date_modify
        e+=1
    
    if tickets.count()>0:
        # print(time,tickets.count())

        time = time/tickets.count()
        return round(time.total_seconds()/60)
    else :
        return 0


def wait_time_Average(tickets,tickets_new):
    print(time_Average(tickets),tickets_new.count())
    return time_Average(tickets)*tickets_new.count()