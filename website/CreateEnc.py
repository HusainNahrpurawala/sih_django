import face_recognition
import os
import pandas as pd
from .__init__ import path

path = path + 'website/'

def encode(name, isGuest):   # USE TRY AND EXCEPT PROPERLY AS SOME IMAGES ARE NOT ENCODABLE
    file = 'encodings.csv'
    if isGuest:
        file = 'guest' + file
        name = 'g' + name

    csv = pd.read_csv(path + file)
    csv = csv.drop(columns=['Unnamed: 0'])
    image = face_recognition.load_image_file(path + 'photos/'+name+'.jpg')
    try:
        enc = face_recognition.face_encodings(image)
        row = [name]

        if len(enc)==0:
            return 100
        if len(enc)!=1:
            return 101

        for i in enc[0]:
            row.append(i)
        csv.loc[csv.shape[0]+1] = row
        csv.to_csv(path + file)
        return 1
    except:
        return 100
