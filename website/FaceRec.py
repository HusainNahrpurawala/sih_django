import face_recognition
import pandas as pd
import cv2, time
import multiprocessing
import numpy as np
import statistics
from CreateLogs import CreateLogs

# SHARED MULTIPROCESSING VARIABLE
face_names = multiprocessing.Manager().Queue(20)


def getEnc():
    csv = pd.read_csv('encodings.csv')
    encodings = []
    names = []

    for i in range(csv.shape[0]):
        print(i)
        innerlist = []
        for j in range(128):
            innerlist.append(csv.iloc[i][str(j + 1)])
        names.append(str(csv.iloc[i]['pk']))
        encodings.append(innerlist)
    return (names, encodings)

def GuestEnc():
    csv = pd.read_csv('guestencodings.csv')
    encodings = []
    names = []

    for i in range(csv.shape[0]):
        print(str(i))
        innerlist = []
        for j in range(128):
            innerlist.append(csv.iloc[i][str(j + 1)])
        names.append(str(csv.iloc[i]['pk']))
        encodings.append(innerlist)
    return (names, encodings)

(names, encodings) = getEnc()  # STORE FROM CSV FILE
(Gname,Gencodings) = GuestEnc()

# METHOD TO BE MULTIPROCESSED
def CompareFace(FaceWebCam, face_names):
    matches = face_recognition.compare_faces(encodings, FaceWebCam,tolerance=0.6)
    name = "UNKNOWN"

    distance = face_recognition.face_distance(encodings, FaceWebCam)
    bestMatch = np.argmin(distance)

    if matches[bestMatch] and distance[bestMatch] < 0.45:
        name = names[bestMatch]
    if name == 'UNKNOWN':
        matchG = face_recognition.compare_faces(Gencodings,FaceWebCam,tolerance=0.6)
        distG = face_recognition.face_distance(Gencodings,FaceWebCam)
        bestMatchG = np.argmin(distG)

        if matchG[bestMatchG] and distG[bestMatchG] < 0.45:
            name = Gname[bestMatchG]
    print(name)
    try:
        face_names.put(name)
    except:
        print("LIST DELETED")


def FaceRec():
    # VIDEO RECORDING AND DETECTION
    videoCapture = cv2.VideoCapture(0)

    # DECLARE VARIABLES
    face_locations = []
    face_encodings = []
    attend = []
    processFrame = True

    while True:
        ret, frame = videoCapture.read()

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)  # REDUCE THE COMPUTATION
        rgbsmall_frame = small_frame[:, :, ::-1]

        if processFrame:
            face_locations = face_recognition.face_locations(rgbsmall_frame)
            face_encodings = face_recognition.face_encodings(rgbsmall_frame, face_locations)
            process = []
            i = 0

            for face in face_encodings:
                # IF A FACE IS DECECTED A PROCESS IS CREATED TO HANDLE THE COMPARISONS
                process.append(multiprocessing.Process(target=CompareFace, args=(face, face_names)))
                process[i].start()
                i = i + 1

        processFrame = not processFrame

        cv2.imshow('Video', frame)

        if face_names.qsize() > 11 or face_names.full():
            temp = []
            for p in process:
                p.join()
            for x in range(face_names.qsize()):
                temp.append(face_names.get())

            attend.append(statistics.mode(temp))
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    videoCapture.release()
    cv2.destroyAllWindows()

    try:
        if attend[0] == 'UNKNOWN':
            for i in range(10):
                print('\a')
                time.sleep(0.1)
            return -1
    except:
        print("FACEREC INTERUPT")
        return -2
    return str(attend[0].split('.')[0])


