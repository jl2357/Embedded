import os
import face_recognition
from picamzero import Camera
from time import sleep
import cv2

class face_rec(object):
    # Global variables
    personID = None
    known_face_encoding = None
    frames = None

    # default constructor
    def __init__(self, personID = 1):
        self.personID = personID
        
        self.video = cv2.VideoCapture(2)
        
    def __del__(self):
        self.video.release()
        
    # encode the known image with the given ID
    def encode_faces(self):
            img = str(self.personID) + ".jpg"
            face_img = face_recognition.load_image_file(f'Known_faces/{img}')
            
            try:
                self.known_face_encoding = face_recognition.face_encodings(face_img)[0]
              
            except:
                print("No faces identified in file " + img)
                os.remove(f'Known_faces/{img}')
              
    def get_frames(self):
        ret, self.frames = self.video.read()
        resized_frame = cv2.resize(self.frames, (420, 420))
        ret, jpeg = cv2.imencode('.jpg', resized_frame)
        return jpeg.tobytes()
        
    # main program
    def recognition(self):
        # take an image of the person for encoding and matching
        cv2.imwrite("detection.jpg", self.frames)
        # load the image taken
        detected_image = face_recognition.load_image_file("detection.jpg")
        
        self.encode_faces()
        
        # encode the taken image
        try:
            detected_encoding = face_recognition.face_encodings(detected_image)[0]
            
        # if there is no face, an error will be thrown. stop the program
        except: 
            print("no face found")
            return False
        
        # compare the known face with the detected face
        try:
            matches = face_recognition.compare_faces([self.known_face_encoding], detected_encoding)
            # if the detected face matches the known face of the correct id, return true
            if matches:
                print("verification success: Identified Person ID " + str(self.personID))
                return True
                
        # if no match is found, an error is thrown. return false
        except:
            print("verification failed, Identified face does not match records")
            return False
        
