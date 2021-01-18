from flask import *
import json
import cv2
import numpy as np 
from PIL import Image
import numpy as np
import io
from google.cloud import vision
import hashlib
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
client = vision.ImageAnnotatorClient()
net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')

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



@app.route("/detect/")
def hello():
    return render_template('file.html')


def group(lst, n):
  for i in range(0, len(lst), n):
    val = lst[i:i+n]
    if len(val) == n:
      yield [val]

@app.route("/getnodes",  methods = ['POST'])
def getnodes():
    theheight = int(request.form['height'])
    thewidth = int(request.form['width']) 
    val = [int(val) for val in request.form['blob'].split(',')]
    groupedval = list_of_lists = [np.array(val[i:i+thewidth], dtype=np.uint8) for i in range(0, theheight*thewidth, thewidth)]
    arr = np.array(groupedval, dtype=np.uint8)
    colorimg = cv2.cvtColor(arr, cv2.COLOR_GRAY2BGR)
    success, encoded_image = cv2.imencode('.jpg', colorimg)
    content2 = encoded_image.tobytes()
    image = vision.Image(content=content2)
    response = client.face_detection(image=image)
    faces = response.face_annotations
    theres = []
    for face in faces:
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                for vertex in face.bounding_poly.vertices])
        p1 = eval(vertices[0])
        p2 = eval(vertices[1])
        p3 = eval(vertices[2])
        p4 = eval(vertices[3])
        theres.append([p1, p2, p3, p4])
    print(theres)




    blob = cv2.dnn.blobFromImage(colorimg, 1/255, (416, 416), (0,0,0), swapRB = True, crop = False)
    net.setInput(blob) #Set input from the network
    output_layers_names = net.getUnconnectedOutLayersNames()
    layerOutputs = net.forward(output_layers_names) #Get Outputs from this function, (run forward pass and obtain outputs at output layer)

    boxes = []
    confidences = []
    class_ids = []

    for output in layerOutputs:
        for detection in output: #Output -> 
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.6 and class_id == 0:
                x = int(detection[0] * thewidth) #Normalized Values
                y = int(detection[1] * theheight)
                w = int(detection[2] * thewidth)
                h = int(detection[4] * theheight)
                boxes.append([x, y, w, h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)

    index = cv2.dnn.NMSBoxes(boxes, confidences, 0.6, 0.4)
    ret = []
    if len(index) > 0:
      for i in index.flatten():
          x, y, w, h = boxes[i]
          ret.append([x, y])
    everything = [ret, theres]

    return make_response(jsonify(everything), 200) 


if __name__ == '__main__':
    app.run(debug = True)