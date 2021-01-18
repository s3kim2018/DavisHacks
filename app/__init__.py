import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': "hackdavis-91e48",
})

db = firestore.client()
app = Flask(__name__)
from app import routing
