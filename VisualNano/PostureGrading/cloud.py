from google.cloud import storage, firestore

from datetime import datetime

# will be a variable sent from the Aural Nano

testName = "testName " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

import os


keyfilename = "cs131-finalproject-musiccoach-817785d8a2c0.json"
storage_client = storage.Client.from_service_account_json(keyfilename)
bucket = storage_client.get_bucket('cs131-music-coach-feedback-media')

db = firestore.Client.from_service_account_json(keyfilename)

def upload_file_to_gcs(user_id, source_file_path, destination_file_name):
    destination_blob_name = f"{user_id}/{destination_file_name}" 

    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_path)

    return blob.public_url

def store_grade_with_files(user_id, grade, local_image_paths):
    
    image_urls = []

    
    for eachPath in local_image_paths:
        image_urls.append(upload_file_to_gcs(user_id, eachPath, testName))

    # use current date as path in cloud storage

    userDocumentName = f"user{user_id}"

    user_ref = db.collection('users').document(userDocumentName)

    gradeCollectionName = "grades"
    gradeDocument = f"{testName}"

    grade_ref = user_ref.collection(gradeCollectionName).document(gradeDocument)


    # add feedback
    grade_data = {
        'grade_value' : grade,
        'image_urls' : image_urls
    }




def add_data():
    doc_ref = db.collection('users').document('user1')
    doc_ref.set({
        'first': 'Ada',
        'last': 'Lovelace',
        'born': 1815
    })

# Function to retrieve data from Firestore
def get_data():
    users_ref = db.collection('users')
    docs = users_ref.stream()
    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')

# Example of adding and getting data
add_data()
get_data()
