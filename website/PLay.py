import time
from FaceRec import *
from CreateLogs import *


def Recognize():
    try:
        while 1:
            a = CreateLogs(FaceRec())

            if a == 0:
                print('UNKNOWN PERSON')
            elif a == -1:
                break
            else:
                print("YOU MAY ENTER/EXIT")
            time.sleep(2)

    except KeyboardInterrupt:
        print("INTERUPT")


Recognize()
