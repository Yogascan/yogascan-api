from flask_restful import Resource
from flask import request
from firebase_setup import db
from firebase_admin import auth

class getUser(Resource):
    def get(self):
        try:
            # Mendapatkan UID dari permintaan JSON
            uid = request.json['uid']

            # Mendapatkan user record dari Firebase Authentication
            user_record = auth.get_user(uid)
            user_email = user_record.email

            # Mendapatkan referensi dokumen dari Firestore berdasarkan UID
            user_ref = db.collection('user').where('uid', '==', uid).stream()

            # Inisialisasi variabel untuk menyimpan data user
            user_info = None

            # Iterasi melalui hasil query untuk mendapatkan data pengguna
            for doc in user_ref:
                user_data = doc.to_dict()  # Konversi dokumen ke dictionary
                user_info = {
                    'email': user_email,
                    'username': user_data.get('username'),
                    'profile_picture': user_data.get('profile_picture')
                }
                break  # Asumsikan hanya ada satu dokumen yang cocok

            # Jika data pengguna ditemukan, kembalikan sebagai respons
            if user_info:
                return user_info, 200
            else:
                return {"message": "User not found"}, 404

        except Exception as e:
            return {"message": "An error occurred: " + str(e)}, 500
