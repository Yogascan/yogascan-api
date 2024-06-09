from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import firebase_admin
from firebase_admin import credentials, auth, firestore
from firebase_setup import db


# Resource untuk login
class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        try:
            user = auth.get_user_by_email(email)
                       
            return {'uid': user.uid}, 200
        except Exception as e:
            return {'message': str(e)}, 401