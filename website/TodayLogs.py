import csv
import pandas as pd
import os
import datetime
from django.contrib.auth.models import User
from .__init__ import path

path = path + 'website/'

def TodayLogs():
    Date = datetime.date.today().strftime("%d/%m/%y")   # TODAYS DATE

    Today = pd.DataFrame(columns=['ID','NAME','DATE','TIME','ENTRY/EXIT'])     # NEW DATAFRAME FOR TODAYS LOGS

    for p in os.listdir(path+'Logs/'):  # ALL CSVS IN FILE
        if p.split('.')[-1] == 'csv':
            csv = pd.read_csv(path + 'Logs/' + p)

            for index in range(csv.shape[0]):
                if csv.iloc[index]['DATE'] ==Date:  # FOR EACH ENTRY WHERE DATE IS EQUAL TO TODAYS DATE
                    pk = int(p.split('.')[0])
                    name = User.objects.get(pk=pk).first_name
                    Today.loc[Today.shape[0]-1] = [pk,name,csv.iloc[index]['DATE'],csv.iloc[index]['TIME'],csv.iloc[index]['ENTRY/EXIT']]

    Today.sort_values('TIME')   # SORT ACCORDING TO TIME // NOT SURE IF WORKS
    Today.to_csv(path +'Today.csv')





