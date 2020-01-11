import csv
import pandas as pd
import os
import datetime
from __init__ import path

path = path + 'Logs/'


def CreateLogs(name):
    if name == -1:
        return 0    # UNKNOWN
    if name ==-2:   # KEYBOARD INTERUPT BY FACEREC
        return -1
    date = datetime.date.today()    # DATE OF ENTRY
    time = datetime.datetime.now()  # TIME OF ENTRY

    if name[0]=='g':
        if os.path.exists(path + 'Guests.csv'):
            logs = pd.read_csv(path + 'Guests.csv')
            logs = logs.drop(columns=['Unnamed: 0'])
            entry = 'EXIT'

            # CHECK WHETHER LAST ENTERED OR EXITED
            for i in range(logs.shape[0]):
                if logs.iloc[logs.shape[0]-1-i]['GUEST ID'] == name:
                    entry = logs.iloc[logs.shape[0]-1-i]['ENTRY/EXIT']
                    break


            if entry == 'ENTRY':
                enterlog = 'EXIT'
            else:
                enterlog = 'ENTRY'

            logs.loc[logs.shape[0]] = [name,date.strftime("%d/%m/%y"), time.strftime("%H:%M:%S"), enterlog]
            logs.to_csv(path + 'Guests.csv')

        else:
            csvfile = open(path +'Guests.csv', 'w')
            filewriter = csv.writer(csvfile, delimiter=',')
            filewriter.writerow(['Unnamed: 0', 'GUEST ID','DATE', 'TIME', 'ENTRY/EXIT'])
            filewriter.writerow([0, name ,date.strftime("%d/%m/%y"), time.strftime("%H:%M:%S"), 'ENTRY'])
            csvfile.close()
        return 1

    else:
        if os.path.exists(path + name + '.csv'):
            logs = pd.read_csv(path + name + '.csv')
            logs = logs.drop(columns=['Unnamed: 0'])
            entry = logs.iloc[logs.shape[0] - 1]['ENTRY/EXIT']

            if entry == 'ENTRY':
                enterlog = 'EXIT'
            else:
                enterlog = 'ENTRY'

            logs.loc[logs.shape[0]] = [date.strftime("%d/%m/%y"), time.strftime("%H:%M:%S"), enterlog]
            logs.to_csv(path + name + '.csv')

        else:
            csvfile = open(path + name + '.csv', 'w')
            filewriter = csv.writer(csvfile, delimiter=',')
            filewriter.writerow(['Unnamed: 0', 'DATE', 'TIME', 'ENTRY/EXIT'])
            filewriter.writerow([0, date.strftime("%d/%m/%y"), time.strftime("%H:%M:%S"), 'ENTRY'])
            csvfile.close()
        return 1

