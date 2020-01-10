import csv
import pandas as pd
import os
import datetime
from __init__ import path

path = path + 'Logs/'


def CreateLogs(name):
    name = str(name)
    date = datetime.date.today()    # DATE OF ENTRY
    time = datetime.datetime.now()  # TIME OF ENTRY

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
    print('LOGGED')

