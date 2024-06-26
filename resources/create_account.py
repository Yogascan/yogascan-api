from flask_restful import Resource
from flask import request
from firebase_setup import db
from firebase_admin import auth

class CreateAccount(Resource):
    def post(self):
        # Extract JSON data from the incoming request
        data = request.get_json()

        # Extract specific fields from the JSON data
        email = data.get('email')
        password = data.get('password')
        username = data.get('username')

        # Check if required fields are present
        if not email or not password or not username:
            return {"error": "Email, password, and username are required"}, 400

        try:
            # Create a new user with the provided email and password
            user = auth.create_user(
                email=email,
                password=password
            )

            # Add the new user's UID and username to the Firestore database
            db.collection('user').add({'uid': user.uid, 'username': username, 'profile_picture': 'https://storage.googleapis.com/yogascan-bucket/profile-picture/profil-user.png'})

            # Return a success message along with the UID
            return {
                "message": "Successfully created new user",
                "uid": user.uid
            }, 201
        except Exception as e:
            # Return an error message if any exception occurs
            return {"error": str(e)}, 400
