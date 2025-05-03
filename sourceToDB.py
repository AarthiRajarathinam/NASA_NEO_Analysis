import streamlit as st
from datetime import datetime as dt
from streamlit_option_menu import option_menu
import mysql.connector as db
import pandas as pd
import re 
import requests
import mysql.connector as db

#Retrieving data from source


def get_data():
    asteroid_data=[]
    target=10000
    API_keys="dxk9AAO9C0X3TVp9mK20g9bGj4uY3vy27sNFl9ii"
    url=f"https://api.nasa.gov/neo/rest/v1/feed?start_date=2024-01-01&end_date=2024-01-07&api_key={API_keys}"

    while len(asteroid_data)<target:

        response=requests.get(url)
        data=response.json()
        details = data["near_earth_objects"]
        
        for date,info in details.items():
            for i in info:
                asteroid_data.append(dict(id=int(i['id']),
                                        neo_reference_id = int(i['neo_reference_id']),
                                        name = re.sub(r'[^\w\s]', '', i['name']),
                                        absolute_magnitude_h = float(i['absolute_magnitude_h']),                                      
                                        estimated_diameter_min_km = float(i['estimated_diameter']['kilometers']['estimated_diameter_min']),
                                        estimated_diameter_max_km = float(i['estimated_diameter']['kilometers']['estimated_diameter_max']),
                                        is_potentially_hazardous_asteroid = bool(i['is_potentially_hazardous_asteroid']),
                                        close_approach_date = dt.strptime(i['close_approach_data'][0]['close_approach_date'],"%Y-%m-%d" ),
                                        relative_velocity_kmph = float(i['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']),
                                        astronomical = float(i['close_approach_data'][0]['miss_distance']['astronomical']),
                                        miss_distance_km = float(i['close_approach_data'][0]['miss_distance']['kilometers']),
                                        miss_distance_lunar = float(i['close_approach_data'][0]['miss_distance']['lunar']),
                                        orbiting_body = i['close_approach_data'][0]['orbiting_body']
                                        
                                    ))
                                            
                if len(asteroid_data)>=target:
                    break
        
            if len(asteroid_data)>=target:
                break  
            
    url = data["links"]["next"]
    return (asteroid_data, url)


asteroid_data, url = get_data()


#######################
# Database connection
########################

connection=db.connect(
    host="localhost",
    user="nasa",
    password="12345678",
    database="NASA_Asteroid",
    auth_plugin='mysql_native_password'
)


curr=connection.cursor()

####################################
# Table creation
#######################################

curr.execute(""" 

    create table asteroids(
                    id int,
                    name varchar(255),
                    absolute_magnitude_h float,
                    estimated_diameter_min_km float,
                    estimated_diameter_max_km float,
                    is_potentially_hazardous_asteroid boolean
          )
          
          
""")

curr.execute(""" 

    create table close_approach(
                    neo_reference_id int,
                    close_approach_date date,
                    relative_velocity_kmph float,
                    astronomical float,
                    miss_distance_km float,
                    miss_distance_lunar float,
                    orbiting_body varchar(255)
    )      
          
""")

############################
# Inserting data into table
##################################

insert_query1=""" insert into asteroids (id,name,absolute_magnitude_h,estimated_diameter_min_km,estimated_diameter_max_km,is_potentially_hazardous_asteroid)
                values(%s,%s,%s,%s,%s,%s)"""
                
for i in asteroid_data:
    values=(i['id'],
            i['name'],
            i['absolute_magnitude_h'],
            i['estimated_diameter_min_km'],
            i['estimated_diameter_max_km'],
            i['is_potentially_hazardous_asteroid'])
    curr.execute(insert_query1,values)
connection.commit()

insert_query2=""" insert into close_approach (neo_reference_id,close_approach_date,relative_velocity_kmph,astronomical,
              miss_distance_km,miss_distance_lunar,orbiting_body)
                values(%s,%s,%s,%s,%s,%s,%s)"""
                
for i in asteroid_data:
    values=(i['neo_reference_id'],
            i['close_approach_date'],
            i['relative_velocity_kmph'],
            i['astronomical'],
            i['miss_distance_km'],
            i['miss_distance_lunar'],
            i['orbiting_body'])
    curr.execute(insert_query2,values)
connection.commit()

curr.close()
connection.close()  
    
