# Put sample resumes in /var/uploads/

# Instruction For This File:
# 1. Get filename
# 2. Get file path in /var/uploads/
# 3. Grab pdf from that uploads file
# 4. Parse information
# 5. Return data in json file
import os
import pathlib
import uuid
import flask
import CertPathway
import PyPDF2
import json
from werkzeug.datastructures import FileStorage
from io import BytesIO

def get_resume_data(resume_data):
    # Declaring variables
    connection = CertPathway.model.get_db()
    filename = resume_data.filename
    #TODO: get logname from flask
    logname = "nskarns"

    # Storing information into the database
    if filename == '':
        flask.abort(400)

    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix.lower()
    uuid_basename = f"{stem}{suffix}"

    path = CertPathway.app.config['UPLOAD_FOLDER']/filename
    resume_data.save(path)

    # Insert resume information into database
    #cur = connection.execute(
    #    "INSERT INTO resumes (filename, username) "
    #    "SELECT ? AS filename, ? AS username "
    #    "WHERE NOT EXISTS (SELECT 1 FROM resumes WHERE filename = ? AND username = ?)",
    #    (filename, logname, filename, logname)
    #)

    # Extracting the words
    words = []
    with open(path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            text = pdf_reader.pages[page_num].extract_text()
            page_words = text.split()
            words.extend(page_words)
    
    # Returning list of words from resume
    return words

def get_interest_form_data(interest_form_data):
    # Spliting up words and returning
    return interest_form_data.split()

def input_user_words(user_words):
    # TODO: Implement function when database is ready
    pass

def grab_certificates(user_words_list):
    # Declaring variables
    certificate_dict = {}

    # TODO: Making file grab into database grab
    # Grabbing inverted index keywords
    with open('CertPathway/misc/inverted_index_keywords.json', 'r') as json_file:
        data = json.load(json_file)
    
    # Looping through words to see if they exist in inverted index
    for user_word in user_words_list:
        if user_word in data:
            for cert_id in data[user_word]:
                if cert_id in certificate_dict:
                    certificate_dict[cert_id] += 1
                else:
                    certificate_dict[cert_id] = 1

    # Return certificate dictionary
    return(certificate_dict)

def grab_all_certificates():
    certificate_dict = {}

    # TODO: Making file grab into database grab
    # Grabbing all possible certificates and setting value to one
    # Do with a connection

    # Hardcoded all certificates in dictionary
    for i in range(0, 11):
        certificate_dict[i] = 1

    # Return certificate dictionary
    return certificate_dict

@CertPathway.app.route('/upload/')
def change_post():
    # Declaring variables
    resume_list = []
    interest_form_list = []
    certificate_list = []
    threshold_met = False
    keyword_threshold = 10
    certificate_threshold = 5

    # Hardcoded resume
    with open('var/uploads/new_york_resume.pdf', 'rb') as f:
        file_content = BytesIO(f.read())
    resume_data = FileStorage(stream=file_content, filename='new_york_resume.pdf')

    # Hardcoded interest form
    interest_form_data = "SSL/TLS Certificate CompTIA A+ Certification PMP Certification"
    
    # TODO: Make these go into effect below
    # Getting resume/interest form data
    #resume_data = flask.request.files.get('', None)
    #interest_form_data = request.form.get('', None)

    # TODO: Make these go in effect below
    # Getting user data in terms of cost, time, and fields of interest
    #cost_data = request.form.get('', None)
    #time_data = request.form.get('', None)
    #fields_of_interest_data = request.form.get('', None)

    # Determing if data exists
    if resume_data is not None:
        resume_list = get_resume_data(resume_data)
    if interest_form_data is not None:
        interest_form_list = get_interest_form_data(interest_form_data)

    # Combining lists
    keyword_list = list(set(resume_list + interest_form_list))

    # Add keyword_list to database
    input_user_words(keyword_list)

    # Determing list of certificates
    if len(keyword_list) > 0:
        certificate_dict = grab_certificates(keyword_list)
    else:
        certificate_dict = grab_all_certificates()

    print(certificate_dict)
    # Determing what certificates meet the parameters
    certificate_keys = certificate_dict.keys()
    for certificate_key in certificate_keys:
        # TODO: Implement this portion with hardcoded values
        # look up certificate in database - grab cost, time, field of interest list
        # compare that data to user data
        # if doesn't meet cost, time, field of interest requirements then remove from database
        pass

    # Determing if enough certificates are in list to continue
    certificate_keys = certificate_dict.keys()
    while threshold_met == False:
        for certificate_key in certificate_keys:
            if certificate_dict[certificate_key] >= keyword_threshold:
                certificate_list.append(certificate_key)
            if len(certificate_list) >= certificate_threshold:
                threshold_met = True
                break
        if threshold_met == False:
            certificate_list = [] 
            keyword_threshold -= 1

    # returing list of certificates to use
    return {"certificates": certificate_list}