import cv2
import numpy as np 
from google.cloud import vision
import io

client = vision.ImageAnnotatorClient()
net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')
classes = []
with open('coco.names', 'r') as f:
    classes = f.read().splitlines()

img = cv2.imread('img/store.jpg')

success, encoded_image = cv2.imencode('.jpg', img)
content2 = encoded_image.tobytes()
image = vision.Image(content=content2)
response = client.face_detection(image=image)
faces = response.face_annotations

for face in faces:
    vertices = (['({},{})'.format(vertex.x, vertex.y)
                for vertex in face.bounding_poly.vertices])

    p1 = eval(vertices[0])
    p2 = eval(vertices[1])
    p3 = eval(vertices[2])
    p4 = eval(vertices[3])
    print(p1)
    print(p4)
    cv2.rectangle(img, (p1[0], p1[1]), (p3[0], p3[1]), (0, 255, 0), 2)
cv2.imshow("hello", img)
cv2.waitKey()
cap = cv2.VideoCapture('test.mp4')
cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)

while True:
    break 
    _, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    curr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    height, width, _ = img.shape

    blob = cv2.dnn.blobFromImage(curr, 1/255, (416, 416), (0,0,0), swapRB = True, crop = False)
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
            if confidence > 0.5:
                x = int(detection[0] * width) #Normalized Values
                y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[4] * height)
                boxes.append([x, y, w, h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)

    index = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_PLAIN
    colors = np.random.uniform(0, 255, size = (len(boxes), 3))
    print(index)
    
    print(index.flatten())
    for i in index.flatten():
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        confidence = str(round(confidences[i]))
        color = colors[i]
        cv2.circle(img, (x, y), 3, color, 2)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()
