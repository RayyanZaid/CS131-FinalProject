from google.cloud import storage, firestore


import os
import cv2
from io import BytesIO

keyfilename = "../cs131-finalproject-musiccoach-817785d8a2c0.json"
storage_client = storage.Client.from_service_account_json(keyfilename)
bucket = storage_client.get_bucket('cs131-music-coach-feedback-media')

db = firestore.Client.from_service_account_json(keyfilename)

def upload_file_to_gcs(frame, destination_blob_name):
    # Initialize the Google Cloud Storage client
    
    # Encode frame to JPEG format in memory
    _, buffer = cv2.imencode('.jpg', frame)
    bio = BytesIO(buffer)

    # Create a blob and upload the file to Google Cloud Storage
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(bio, content_type='image/jpeg')

    # Make the blob publicly viewable (if needed)
    blob.make_public()

    # Return the public URL of the uploaded file
    return blob.public_url

def store_grade_with_files(username, testName, postureGrade, feedbackArray):
    
    feedbackAndImages = []

    i = 0
    for eachFeedback in feedbackArray:
        eachFeedbackText = eachFeedback[0]
        eachImage = eachFeedback[1]
        bucketLocationPath = f"{username}/{testName}-{i}"
        feedbackAndImages.append({
            'feedbackText': eachFeedbackText,
            'feedbackImage' : upload_file_to_gcs(eachImage, bucketLocationPath)
        })
        i += 1

    # use current date as path in cloud storage

    try:
        currentTestData = {
            'name': testName,
            'postureGrade': postureGrade,
            'postureFeedbackArray': feedbackAndImages,
        }

        # Get a reference to the document for the username
        user_ref = db.collection('users').document(username)

        # Check if the document exists
        doc = user_ref.get()
        if doc.exists:
            # Document exists, update it
            user_ref.update({
                'tests': firestore.ArrayUnion([currentTestData])
            })
        else:
            # Document does not exist, create it
            user_ref.set({
                'tests': [currentTestData]
            }, merge=True)
    except Exception as e:
        raise e





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


if __name__ == '__main__':
    # Example of adding and getting data
    add_data()
    get_data()
