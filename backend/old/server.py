from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os
import base64
import json
import numpy as np
import cv2
import face_recognition as fr 



#compute euclidean distance between 2 face encodings and return True or False
def computeDistance(enc1 , enc2 , Threshold=0.5) : 
    dist=np.linalg.norm(enc1-enc2)
    if dist > Threshold :
        return False
    else :
        return True

# if there is no data saved for this name on the database then this function will return an empty lis
# else it will return a list containing a dictionary of users data as [{'name':'' , 'embedding':''}]
def GetUserdata(name) :

    userdata=json.loads(users_schema.dumps(User.query.filter_by(Name='waly')).data)

    return userdata


#this extracts the embedding from the data returned from GetUserdata
def GetEmbeddingFromData(data):
    
    embedding=np.array(json.loads(data[0]['Embedding']))
    return embedding


#this function maps the image to b64 string to be sent in response or saved in database
def imageToUri(image):
    x, buffer=cv2.imencode('.png',image)
    png_as_text=base64.b64encode(buffer)
    uri="data:image/png;base64,"+str(png_as_text)[2:-1]

    return uri
#this function takes the image from the response as a b64 string and return it as a cv2 image
def data_uri_to_cv2_img(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


#This function detects face in image and draws a redbox on it then return the image with the redbox 
def DetectFace(frame):
    face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    frame_gray= cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    face= face_cascade.detectMultiScale(frame_gray, 1.3, 5)
    if np.any(face):
        for(x,y,w,h) in face :
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0 , 255), 2)
            return frame 
        
    else:

        return -1


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'Smith.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

SQLALCHEMY_TRACK_MODIFICATIONS=False 

CORS(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(120), unique=True)
    # Name = db.Column(db.String(120), unique=False)
    Embedding = db.Column(db.String(10000), unique=True)

    def __init__(self, Name , Embedding):
        # self.Name=Name
        self.Name = Name
        self.Embedding=Embedding

class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('Name','Embedding')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


@app.route("/",methods=['GET'])
@app.route("/register", methods=['POST','GET'])
def register():

    if(request.method == 'POST' ) :
        
        name = request.json.get('name')
        image = request.json.get('image') # base_64 string

        try:
            if name is None or image is None:
                return '',400 # missing arguments
            else:
                image= data_uri_to_cv2_img(image) #from base64 to cv2 image
                image= cv2.cvtColor(image,cv2.COLOR_BGR2RGB) # opencv default channels are (B,G,R) so i change it to RGB to send it to face_recognition model as it take image as rgb and uses PIL library
                embedding=fr.face_encodings(image)
                embedding=np.array(embedding).tolist()
                embedding=json.dumps(embedding)
                user = User(Name = name, Embedding = embedding)
                db.session.add(user)
                db.session.commit()
                return jsonify({ "Status": 'Registered Successfully' , 'Embedding' : embedding })
        except:
            return 'Name already exists',403

#this to make a redbox over the image and return it to the registration process
@app.route("/checkFace", methods=['POST'])
def checkface() :
    image=request.json.get('image')
    im = imageToUri(DetectFace(data_uri_to_cv2_img(image)))
    return jsonify({'image': format(im) })

@app.route("/login", methods=['POST'])
def login():
    imageflag=request.json.get('imageFlag')#if true an image is recieved in request , if false an embedding file is uploaded
    name = request.json.get('name')
    userdata=GetUserdata(name) 
                               
    if (len(userdata)==0):
        return "No registered user with this Name",400
    
    else :

        if imageflag :
            image = request.json.get('image')   
            image=data_uri_to_cv2_img(image)
            image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            capturedEmbedding=np.array(fr.face_encodings(image))

        else :
            capturedEmbedding=json.loads(request.json.get('embedding'))
            capturedEmbedding=np.array(capturedEmbedding)
            
       
        #for getting user saved embedding on the database 
        userSavedEmbedding=GetEmbeddingFromData(userdata)
        permission=computeDistance(userSavedEmbedding[0],capturedEmbedding[0])
        if(permission):
            return jsonify( { "Status": permission })
        else :
            return "Not the face of user",403
if __name__ == '__main__':
    app.run(debug=True)


