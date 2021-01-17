# run `export GOOGLE_APPLICATION_CREDENTIALS="C:\Users\Kim\Documents\hack_davis_backend\key.json"`
# will separate into `__init__.py` , `routings.py` , `run.py` later

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import *

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup_user():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    email    = request.form['email']
    company  = request.form['company']
    password = request.form['password']

    new_user = db.collection('users').document(email)
    new_user.set({
        'email': email,
        'company': company,
        'password': password
    })
    return render_template('login.html')

@app.route('/login')
def login_user():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email    = request.form['email']
    password = request.form['password']

    user = db.collection('users').document(email).get()
    if user.exists:
        # fix render to future homepage!!
        return render_template('index.html')
    else:
        print("Error: No user associated with email.")
        return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
