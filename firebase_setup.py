import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import storage

# Initialize Firebase app
cred = credentials.Certificate("./serviceAccount.json")
firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

# Initialize Google Cloud Storage client
storage_client = storage.Client.from_service_account_json('./yogascan-bucket-SA.json')
