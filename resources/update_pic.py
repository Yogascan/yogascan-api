from flask_restful import Resource
from flask import request
from google.cloud import storage
from firebase_setup import db, storage_client
import urllib.parse

class UpdateProfPic(Resource):
    def post(self):
        try:
            uid = request.form.get('uid')
            if not uid:
                return {"message": "UID is required"}, 400
            
            if 'profile_picture' not in request.files:
                return {"message": "No file part"}, 400
            
            file = request.files['profile_picture']
            if file.filename == '':
                return {"message": "No selected file"}, 400
            
            # Fetch the user document by UID
            users_ref = db.collection('user')
            query = users_ref.where('uid', '==', uid).limit(1)
            results = query.stream()
            user_doc = None

            for doc in results:
                user_doc = doc
                break
            
            if user_doc is None:
                return {"message": "User not found"}, 404

            user_data = user_doc.to_dict()
            old_profile_picture_url = user_data.get('profile_picture', None)

            # Cloud Storage bucket name
            bucket_name = 'yogascan-bucket'
            bucket = storage_client.bucket(bucket_name)

            # Upload the new profile picture
            new_file_name = f"profile-picture/{uid}/{file.filename}"
            blob = bucket.blob(new_file_name)
            blob.upload_from_file(file, content_type=file.content_type)

            # Delete the old profile picture if it exists and is not the default
            default_profile_picture = "https://storage.googleapis.com/yogascan-bucket/profile-picture/profil-user.png"
            if old_profile_picture_url and old_profile_picture_url != default_profile_picture:
                old_blob_name = '/'.join(old_profile_picture_url.split('/')[-3:])
                old_blob_name = urllib.parse.unquote(old_blob_name)  # Decode any URL-encoded characters
                old_blob = bucket.blob(old_blob_name)
                old_blob.delete()

            # Update Firestore with the new profile picture URL
            new_profile_picture_url = blob.public_url
            user_doc.reference.update({"profile_picture": new_profile_picture_url})

            return {"message": "Profile picture updated successfully", "profile_picture": new_profile_picture_url}, 200

        except Exception as e:
            print(f"Exception: {str(e)}")
            return {"message": "An error occurred: " + str(e)}, 500
