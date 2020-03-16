#!/usr/bin/env python

import sqlite3

from glob import glob
from datetime import datetime
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta


# Path to database file
#DATABASE = glob("./calls_20200305.db")[0]
DATABASE = 'calls_20200305.db'

def extract_column_names(query):
    """
    This attempts to extract all the keys from
    the SELECT part of the query to build a json
    response
    """
    line = next(
        filter(
            lambda a: "SELECT" in a,
            query.split("\n")
        ))\
        .replace("SELECT", "")\
        .strip()
    column_name = [n.strip() for n in line.split(",")]
    return column_name


def build_json_response(db_response, keys):
    json_response = []
    for row in db_response:
        d = {}

        for i, key in enumerate(keys):
            if key in ["lat", "lon"]:
                d[key] = float(row[i])
            elif key == "datetime":
                d[key] = datetime.strptime(row[i], "%Y-%m-%d %H:%M:%S")
            else:
                d[key] = row[i]

        json_response.append(d)
    return json_response


def query_db(query, args=(), tuples=True, database=DATABASE):
    """
    Use this method to execute sql queries in a database.
    Some examples of making SELECT queries:
    https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/


    tuples: if set to true, you just get a list of tuples
        matching the query. Otherwise an attempt will be
        made to return a dictionary with key/value pairs
        which may not succed for some queries.
    """
    db = sqlite3.connect(DATABASE)
    cur = db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    db.close()
    keys = extract_column_names(query)
    if tuples:
        return rv
    else:
        return build_json_response(rv, keys)


def data_to_df(data):
    data_dict = pd.DataFrame(columns = ['day', 'day_of_week', 'urgency_low', 'urgency_middle', 
                                        'urgency_high', 'ambulance', 'fire-bridage',
                                        'police', 'helicopter'])
        
    newday = True 
    temp_urg_low = 0
    temp_urg_middle = 0
    temp_urg_high = 0
    temp_am = 0
    temp_pol = 0
    temp_fir = 0
    temp_hel = 0
    for i in range(len(data)):
        if(data[i]['datetime'].strftime("%b %d %Y") != data[i-1]['datetime'].strftime("%b %d %Y")
           and i > 0):
            newday = True          
            data_dict = data_dict.append({'day' : data[i-1]['datetime'].strftime("%Y %m %d"), 
                              'day_of_week':  data[i-1]['datetime'].strftime("%A"), 
                              'urgency_low' : temp_urg_low, 
                              'urgency_middle' : temp_urg_middle, 
                              'urgency_high' : temp_urg_high, 
                              'ambulance' : temp_am, 'fire-bridage': temp_fir,
                              'police' : temp_pol, 'helicopter' : temp_hel},            
                               ignore_index= True)          
            
        if(newday == True or i == 0):
            temp_urg_low = 0
            temp_urg_middle = 0
            temp_urg_high = 0
            temp_am = 0
            temp_pol = 0
            temp_fir = 0
            temp_hel = 0
            newday = False
         
        if(data[i]['urgency'] == 'H'):
            temp_urg_high += 1
        elif(data[i]['urgency'] == 'M'):
            temp_urg_middle += 1
        elif(data[i]['urgency'] == 'L'):
            temp_urg_low += 1
        
        if(data[i]['service'] == 'ambulance'):
            temp_am += 1
        elif(data[i]['service'] == 'fire-brigade'):
            temp_fir += 1
        elif(data[i]['service'] == 'helicopter'):
            temp_hel += 1
        elif(data[i]['service'] == 'police'):
            temp_pol += 1
            
        
    print(data_dict)
    return(data_dict)

    
def basic_bar_graph(df):
    df = df.sort_values(by=['day'])  
    df.plot(kind='bar',x='day',y=['urgency_low', 'urgency_middle', 'urgency_high'])    
    df.plot(kind='bar',x='day',y=['ambulance', 'police', 'fire-bridage', 'helicopter'])
    
    
def basic_trends(df):
    #trend per day of week
    day_of_week = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df_week = df.groupby(['day_of_week']).sum().reindex(day_of_week)
    df_week.plot(y=['urgency_low', 'urgency_middle', 'urgency_high'])    
    df_week.plot(y=['ambulance', 'police', 'fire-bridage', 'helicopter'])
    plt.show()
    
    #
    df['urgency_middle'].rolling(3).mean().plot()
    plt.show()
    
        
if __name__ == "__main__":
    query = """
    SELECT datetime, urgency, service
    FROM calls
    WHERE region = '22 BZO Brabant-Zuidoost'
    LIMIT 1000
    """
    
    
    #print("Tuples response:")
    #print(query_db(query))
    
    data = query_db(query, tuples=False)
    #print("Json response:")
    #print(data)
    
    df = data_to_df(data)
    basic_bar_graph(df)
    basic_trends(df)
    
    
