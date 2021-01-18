import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': "hackdavis-91e48",
})

# Not sure if we need this, but keeping here for reference
config = {
  "apiKey": "AIzaSyC_8PaKkYuSaxcKaQ9I1lKExI0Xs_0qZgU",
  "authDomain": "hackdavis-91e48.firebaseapp.com",
  "databaseURL": "https://hackdavis-91e48-default-rtdb.firebaseio.com",
  "projectId": "hackdavis-91e48",
  "storageBucket": "hackdavis-91e48.appspot.com",
  "messagingSenderId": "296786520370",
  "appId": "1:296786520370:web:141b4d4a904bc22e518f2b",
  "measurementId": "G-RHBCW5B7XM"
}

db = firestore.client()
app = Flask(__name__)
from app import routing
