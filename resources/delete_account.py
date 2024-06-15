from flask_restful import Resource
from flask import request
from firebase_setup import db
from firebase_admin import auth

class DeleteAccount(Resource):
    def delete(self):
        try:
            uid = request.json['uid']

            auth.delete_user(uid)
            return {"message": "Account has been successfully deleted"}, 200
        except Exception as e:
            return {"message": "An error occurred: " + str(e)}, 500
        
