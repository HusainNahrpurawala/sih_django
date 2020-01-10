import face_recognition
import pandas as pd
import cv2
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


(names, encodings) = getEnc()  # STORE FROM CSV FILE


# METHOD TO BE MULTIPROCESSED
def CompareFace(FaceWebCam, face_names):
    matches = face_recognition.compare_faces(encodings, FaceWebCam)
    name = "UNKNOWN"

    distance = face_recognition.face_distance(encodings, FaceWebCam)
    bestMatch = np.argmin(distance)
    if matches[bestMatch]:
        name = names[bestMatch]
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
            print("ATTENDANCE UPDATED")
            attend.append(statistics.mode(temp))
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    videoCapture.release()
    cv2.destroyAllWindows()

    return int(attend[0].split('.')[0])

CreateLogs(FaceRec())

