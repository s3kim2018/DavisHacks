from app import app, db
from flask import render_template, request
import re

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

    comp = db.collection('companies').document(company).get()
    if not comp.exists:
        new_company = db.collection('companies').document(company)
        new_company.set({
            'company': company,
            'images': []
        })
    return render_template('login.html')

@app.route('/login')
def login_user():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email    = request.form['email']
    password = request.form['password']

    user     = db.collection('users').document(email).get()

    if user.exists:
        user_info = user.to_dict()
        correct   = user_info['password']
    
        if re.match(password, correct):
            return render_template('home.html', user=user_info)
        else:
            print("Error: Incorrect password")
            return render_template('login.html')
    else:
        print("Error: No user associated with email.")
        return render_template('login.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    upload  = request.get_json()
    url     = str(upload.get('url'))
    company = str(upload.get('company'))

    comp    = db.collection('companies').document(company)
    images  = comp.get().to_dict()['images']
    comp.update({
        'images': images + [url]
    })
