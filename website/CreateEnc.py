import face_recognition
import os
import pandas as pd
from .__init__ import path

path = path + 'website/'

def encode(name, isGuest):   # USE TRY AND EXCEPT PROPERLY AS SOME IMAGES ARE NOT ENCODABLE
    file = 'encodings.csv'
    if isGuest: file = 'guest' + file

    csv = pd.read_csv(path + file)
    csv = csv.drop(columns=['Unnamed: 0'])
    image = face_recognition.load_image_file(path + 'photos/'+'g'+name+'.jpg')
    enc = face_recognition.face_encodings(image)[0]

    row = [name]
    for i in enc:
        row.append(i)
    csv.loc[csv.shape[0]+1] = row
    csv.to_csv(path + file)
