import streamlit as st
from datetime import datetime as dt
from streamlit_option_menu import option_menu
import mysql.connector as db
import pandas as pd
import re 
import requests


st.set_page_config(layout="wide")

page_element="""
<style>
[data-testid="stAppViewContainer"]{
  background-image: url("https://cdn.wallpapersafari.com/88/75/cLUQqJ.jpg");
  background-size: cover;
}
</style>
"""

#st.markdown(page_element, unsafe_allow_html=True)

# css for the button
button_style = """
    <style>
    .stButton > button {
        width: 200px;
        height: 50px;
        font-size: 20px;
    }
    </style>
    """

# Apply the custom CSS
st.markdown(button_style, unsafe_allow_html=True)



st.markdown("""
<style>
.big-font {
    font-size:75px !important;
    color: darkgreen;
    font-style: bold;
    font-family: 'Courier New', Courier, monospace;
    text-align: center;
    font-weight: bold;  
    background-color: white;
</style>

""", unsafe_allow_html=True)


st.markdown('<p class="big-font"><img src="https://static.vecteezy.com/system/resources/previews/026/761/681/non_2x/cartoon-flying-burning-space-asteroid-with-craters-and-bumps-isolated-stone-with-fire-vector.jpg" width = 200> NASA NEO Analyzer <img src="https://static.vecteezy.com/system/resources/previews/011/453/498/large_2x/meteorite-space-outer-sticker-free-vector.jpg" width = 150></p>', unsafe_allow_html=True)

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
##################################################################################
#   Database connectivity
###########################################################################################

def queries_fn():

    connection=db.connect(
        host="localhost",
        user="nasa",
        password="12345678",
        database="NASA_Asteroid",
        auth_plugin='mysql_native_password'
    )


    curr=connection.cursor()



    # to fetch the data from Asteroid table
    curr.execute("SELECT * FROM asteroids")
    data=curr.fetchall()

    df_asteroid=pd.DataFrame(data,columns=[i[0] for i in curr.description])


    # to fetch the data from Close_approach table

    curr.execute("SELECT * FROM close_approach")
    data1=curr.fetchall()

    df_closeapp=pd.DataFrame(data1,columns=[i[0] for i in curr.description])

    curr.close()
    connection.close()  


    #####################################################################################


        
        

    Questions = {1:"1.Count how many times each asteroid has approached Earth",
                2:"2.Average velocity of each asteroid over multiple approaches",
                3:"3.List top 10 fastest asteroids",
                4:"4.Find potentially hazardous asteroids that have approached Earth more than 3 times",
                5:"5.Find the month with the most asteroid approaches",
                6:"6.Get the asteroid with the fastest ever approach speed",
                7:"7.Sort asteroids by maximum estimated diameter (descending)",
                8:"8.Asteroids whose closest approach is getting nearer over time(Hint: Use ORDER BY close_approach_date and look at miss_distance)",
                9:"9.Display the name of each asteroid along with the date and miss distance of its closest approach to Earth",
                10:"10.List names of asteroids that approached Earth with velocity > 50,000 km/h",
                11:"11.Count how many approaches happened per month",
                12:"12.Find asteroid with the highest brightness (lowest magnitude value)",
                13:"13.Get number of hazardous vs non-hazardous asteroids",
                14:"14.Find asteroids that passed closer than the Moon (lesser than 1 LD), along with their close approach date and distance",
                15:"15.Find asteroids that came within 0.05 AU(astronomical distance)",
                16:"16.Find the asteroid with the largest miss distance from Earth",
                17:"17.Find the asteroid with the largest diameter and its corresponding name",
                18:"18.Find asteroid with the lowest brightness (highest magnitude value)",
                19:"19.Find the average velocity of asteroids on all available dates",
                20:"20.Find the potentially hazardous asteroids that have the highest velocity"}


    #  Selecting the queries

    option = st.selectbox(
        "",
        ("1.Count how many times each asteroid has approached Earth",
        "2.Average velocity of each asteroid over multiple approaches",
        "3.List top 10 fastest asteroids",
        "4.Find potentially hazardous asteroids that have approached Earth more than 3 times",
        "5.Find the month with the most asteroid approaches",
        "6.Get the asteroid with the fastest ever approach speed",
        "7.Sort asteroids by maximum estimated diameter (descending)",
        "8.Asteroids whose closest approach is getting nearer over time(Hint: Use ORDER BY close_approach_date and look at miss_distance)",
        "9.Display the name of each asteroid along with the date and miss distance of its closest approach to Earth",
        "10.List names of asteroids that approached Earth with velocity > 50,000 km/h",
        "11.Count how many approaches happened per month",
        "12.Find asteroid with the highest brightness (lowest magnitude value)",
        "13.Get number of hazardous vs non-hazardous asteroids",
        "14.Find asteroids that passed closer than the Moon (lesser than 1 LD), along with their close approach date and distance",
        "15.Find asteroids that came within 0.05 AU(astronomical distance)",
        "16.Find the asteroid with the largest miss distance from Earth",
        "17.Find the asteroid with the largest diameter and its corresponding name",
        "18.Find asteroid with the lowest brightness (highest magnitude value)",
        "19.Find the average velocity of asteroids on all available dates",
        "20.Find the potentially hazardous asteroids that have the highest velocity"
        
        
        ),
        index=None,
        placeholder="Select your query...",
    )

    st.write("You selected:", option)

    for i in Questions.keys():
        if option == Questions[i]:
            if i==1:
                # 1.Count how many times each asteroid has approached Earth
                approach_count = df_closeapp.groupby(['neo_reference_id'])['close_approach_date'].count().reset_index(name='approach_count')
                approach_count['approach_count'] = approach_count['approach_count'].astype(int)
                st.write("Count how many times each asteroid has approached Earth:")       
                st.dataframe(approach_count, hide_index=True)
            elif i==2: 
                # 2. Average velocity of each asteroid over multiple approaches
                avg_velocity = df_closeapp.groupby(['neo_reference_id'])['relative_velocity_kmph'].mean().reset_index(name='average_velocity_kilometers_per_hour')
                st.write("Average velocity of each asteroid over multiple approaches:")
                st.dataframe(avg_velocity)
            elif i==3:
                # 3. List top 10 fastest asteroids
                fast_astr=df_closeapp.drop_duplicates(subset=['neo_reference_id'])
                fast_astr['relative_velocity_kmph'] = fast_astr['relative_velocity_kmph'].astype(float).round(2)
                fastest_asteroids = fast_astr.nlargest(10, 'relative_velocity_kmph')[['neo_reference_id', 'relative_velocity_kmph']]
                st.write("Top 10 fastest asteroids:")           
                st.dataframe(fastest_asteroids.style.format({'relative_velocity_kmph':'{:.2f}'}), hide_index=True)
            elif i==4:  
                # 4. Find potentially hazardous asteroids that have approached Earth more than 3 times
                hazard_astr = df_asteroid[ df_asteroid['is_potentially_hazardous_asteroid'] == 1 ]
                haz=hazard_astr.groupby(['id','name']) ['is_potentially_hazardous_asteroid'].count().reset_index(name="Potentially hazardous asteroids that have approached Earth more than 3 times")
                st.dataframe(haz)
            elif i==5:      
                # 5. Find the month with the most asteroid approaches
                approach_count1 = df_closeapp.groupby(['neo_reference_id','close_approach_date'])['close_approach_date'].count().reset_index(name='approach_count')
                approach_count1['approach_count'] = approach_count1['approach_count'].astype(int)
                approach_count1['close_approach_date'] = pd.to_datetime(approach_count1['close_approach_date'])
                approach_count1['month'] = approach_count1['close_approach_date'].dt.month
                st.write("The month with the most asteroid approaches is:")
                st.dataframe(approach_count1['month'].drop_duplicates(), hide_index=True)
            elif i==6:
                # 6. Get the asteroid with the fastest ever approach speed
                fastest_approach = df_closeapp.nlargest(1, 'relative_velocity_kmph')[['neo_reference_id', 'relative_velocity_kmph']]
                st.write("The asteroid with the fastest ever approach speed is:")      
                st.dataframe(fastest_approach, hide_index=True)
            elif i==7:
                # 7. Sort asteroids by maximum estimated diameter (descending)
                sorted_asteroids = df_asteroid.sort_values(by='estimated_diameter_max_km', ascending=False)[['name', 'estimated_diameter_max_km']].drop_duplicates()
                sorted_asteroids = pd.DataFrame(sorted_asteroids, columns=['name', 'estimated_diameter_max_km'])  
                st.write("Asteroids sorted by maximum estimated diameter (descending):")
                st.dataframe(sorted_asteroids, hide_index=True)
            elif i==8:
                # 8. Asteroids whose closest approach is getting nearer over time(Hint: Use ORDER BY close_approach_date and look at miss_distance)
                df_closeapp['close_approach_date'] = pd.to_datetime(df_closeapp['close_approach_date'])
                df_closeapp['miss_distance_km'] = df_closeapp['miss_distance_km'].astype(float)     
                df_closeapp['miss_distance_km'] = df_closeapp['miss_distance_km'].round(2)
                df_closeapp['close_approach_date'] =df_closeapp['close_approach_date'].dt.date
                st.write("Asteroids whose closest approach is getting nearer over time:")
                st.dataframe(df_closeapp[['neo_reference_id', 'close_approach_date', 'miss_distance_km']].sort_values(by='close_approach_date'), hide_index=True)
            elif i==9:
                # 9. Display the name of each asteroid along with the date and miss distance of its closest approach to Earth
                asteroid_dt_dist= pd.merge(df_asteroid, df_closeapp, how= 'inner', left_on='id', right_on='neo_reference_id')[['name', 'close_approach_date', 'miss_distance_km']].drop_duplicates(subset=['name'])
                st.write("The name of each asteroid along with the date and miss distance of its closest approach to Earth:")
                st.dataframe(asteroid_dt_dist, hide_index=True)
            elif i==10:
                # 10. List names of asteroids that approached Earth with velocity > 50,000 km/h
                fast_asteroids = df_closeapp[df_closeapp['relative_velocity_kmph'] > 50000][['neo_reference_id', 'relative_velocity_kmph']].drop_duplicates(subset=['neo_reference_id'])
                st.write("Names of asteroids that approached Earth with velocity > 50,000 km/h:")          
                st.dataframe(fast_asteroids, hide_index=True)
            elif i==11:
                # 11. Count how many approaches happened per month
                approach_count2 = df_closeapp.copy()
                approach_count2['close_approach_date'] = pd.to_datetime(approach_count2['close_approach_date'])      
                #approach_count2['close_approach_date'] = approach_count2['close_approach_date'].dt.date
                approach_count2['month'] = approach_count2['close_approach_date'].dt.month      
                st.write("Count how many approaches happened per month:")
                st.dataframe(approach_count2['close_approach_date'].dt.month.value_counts().reset_index(name='approach_count').rename(columns={'index': 'month'}), hide_index=True)
            elif i==12:
                # 12. Find asteroid with the highest brightness (lowest magnitude value)
                highest_brightness = df_asteroid[df_asteroid['absolute_magnitude_h'] == df_asteroid['absolute_magnitude_h'].min()]
                highest_brightness_asteroid = highest_brightness[['name', 'absolute_magnitude_h']].drop_duplicates(subset=['name'])         
                st.write("The asteroid with the highest brightness (lowest magnitude value) is:")
                st.dataframe(highest_brightness_asteroid, hide_index=True)
            elif i==13:
                # 13. Get number of hazardous vs non-hazardous asteroids  
                hazardous_count = df_asteroid['is_potentially_hazardous_asteroid'].value_counts().reset_index()
                hazardous_count.columns = ['is_potentially_hazardous_asteroid', 'count']        
                st.write("Number of hazardous vs non-hazardous asteroids:")
                st.dataframe(hazardous_count, hide_index=True)
            elif i==14:
                # 14. Find asteroids that passed closer than the Moon (lesser than 1 LD), along with their close approach date and distance
                df_closeapp['miss_distance_km'] = df_closeapp['miss_distance_km'].astype(float)
                df_closeapp['miss_distance_km'] = df_closeapp['miss_distance_km'].round(2)              
                close_approach_closer_than_moon = df_closeapp[df_closeapp['miss_distance_km'] < 384400][['neo_reference_id', 'close_approach_date', 'miss_distance_km']].drop_duplicates(subset=['neo_reference_id'])           
                st.write("Asteroids that passed closer than the Moon (lesser than 1 LD):")
                st.dataframe(close_approach_closer_than_moon, hide_index=True)
            elif i==15:
                # 15. Find asteroids that came within 0.05 AU(astronomical distance)
                df_closeapp['astronomical'] = df_closeapp['astronomical'].astype(float)
                df_closeapp['astronomical'] = df_closeapp['astronomical'].round(2)              
                st.write("Asteroids that came within 0.05 AU:")
                st.dataframe(df_closeapp[df_closeapp['astronomical'] < 0.05][['neo_reference_id', 'close_approach_date', 'astronomical']].drop_duplicates(subset=['neo_reference_id']), hide_index=True)
            elif i==16:
                # 16. Find the asteroid with the largest miss distance from Earth      
                largest_miss_distance = df_closeapp[df_closeapp['miss_distance_km'] == df_closeapp['miss_distance_km'].max()]
                largest_miss_distance_asteroid = largest_miss_distance[['neo_reference_id', 'close_approach_date', 'miss_distance_km']].drop_duplicates(subset=['neo_reference_id'])        
                st.write("The asteroid with the largest miss distance from Earth is:")
                st.dataframe(largest_miss_distance_asteroid, hide_index=True)
            elif i==17:
                # 17. Find the asteroid with the largest diameter and its corresponding name
                largest_diameter = df_asteroid[df_asteroid['estimated_diameter_max_km'] == df_asteroid['estimated_diameter_max_km'].max()]
                large_asteroid= largest_diameter[['name', 'estimated_diameter_max_km']].drop_duplicates(subset=['name'])
                st.write("The asteroid with the largest diameter is:")
                st.dataframe(large_asteroid, hide_index=True)
            elif i==18:
                # 18. Find asteroid with the lowest brightness (highest magnitude value)
                lowest_brightness = df_asteroid[df_asteroid['absolute_magnitude_h'] == df_asteroid['absolute_magnitude_h'].max()]
                lowest_brightness_asteroid = lowest_brightness[['name', 'absolute_magnitude_h']].drop_duplicates(subset=['name'])         
                st.write("The asteroid with the lowest brightness (highest magnitude value) is:")
                st.dataframe(lowest_brightness_asteroid, hide_index=True)
            elif i==19:
                # 19. Find the average velocity of asteroids on all available dates
                df_closeapp['close_approach_date']=pd.to_datetime(df_closeapp['close_approach_date'])
                df_closeapp['date'] = df_closeapp['close_approach_date'].dt.date
                avg_velocity_all_dates = df_closeapp.groupby(['date'])['relative_velocity_kmph'].mean().reset_index(name='average_velocity_kilometers_per_hour')
                st.write("The average velocity of asteroids on all available dates:")  
                st.dataframe(avg_velocity_all_dates, hide_index=True)
            elif i==20:
                # 20. Find the potentially hazardous asteroids that have the highest velocity
                hazard_astr = df_asteroid[df_asteroid['is_potentially_hazardous_asteroid'] == 1]        
                hazard_astr = pd.merge(hazard_astr, df_closeapp, how='inner', left_on='id', right_on='neo_reference_id')
                highest_velocity_hazardous = hazard_astr.nlargest(1, 'relative_velocity_kmph')[['name', 'relative_velocity_kmph']]      
                st.write("The potentially hazardous asteroid with the highest velocity is:")
                st.dataframe(highest_velocity_hazardous, hide_index=True)   
            


# Sidebar with multiple tabs
with st.sidebar:
    selected = option_menu(
        menu_title="Choose your option", 
        options=["Filters", "Queries"], 
        icons=["folder", "calendar"],  
        menu_icon="cast",  # optional
        default_index=0,  # optional
    )


def filtered_date(df,attr1val, attr2val):
    #st.write("Selected date range:", attr1val, "to", attr2val)
    #convert the date columns to datetime format
    df['close_approach_date'] = pd.to_datetime(df['close_approach_date'])
    df['close_approach_date'] = df['close_approach_date'].dt.date
    # Convert the selected date range to datetime.date objects
    attr1val = pd.to_datetime(attr1val).date()
    attr2val = pd.to_datetime(attr2val).date()
    # Filter the DataFrame based on the selected date range
    filtered_date_range = df[(df['close_approach_date'] >= attr1val) & (df['close_approach_date'] <= attr2val)]
    #st.dataframe(filtered_date_range, hide_index=True)
    return filtered_date_range

def filter_min_magnitude(df, attribval1, attribval2):
    #st.write("Selected Min Magnitude:", attribval1, "to", attribval2)
    # Filter the DataFrame based on the selected date range
    filtered_magnitude = df[(df['absolute_magnitude_h'] >= attribval1) & (df['absolute_magnitude_h'] <= attribval2)]
    #st.dataframe(filtered_magnitude, hide_index=True)
    return filtered_magnitude

def filter_min_estimated_diameter(df, attribval1, attribval2):
    #st.write("Selected Min Estimated Diameter:", attribval1, "to", attribval2)
    # Filter the DataFrame based on the selected date range
    filtered_estimated_diameter = df[(df['estimated_diameter_min_km'] >= attribval1) & (df['estimated_diameter_max_km'] <= attribval2)]
    #st.dataframe(filtered_estimated_diameter, hide_index=True)
    return filtered_estimated_diameter

def filter_max_estimated_diameter(df, attribval1, attribval2):
    #st.write("Selected Max Estimated Diameter:", attribval1, "to", attribval2)
    # Filter the DataFrame based on the selected date range
    filtered_estimated_diameter = df[(df['estimated_diameter_min_km'] >= attribval1) & (df['estimated_diameter_max_km'] <= attribval2)]
    #st.dataframe(filtered_estimated_diameter, hide_index=True)
    return filtered_estimated_diameter

def filter_relative_velocity(df, attribval1, attribval2):
    #st.write("Selected Relative Velocity:", attribval1, "to", attribval2)
    # Filter the DataFrame based on the selected date range
    filtered_velocity = df[(df['relative_velocity_kmph'] >= attribval1) & (df['relative_velocity_kmph'] <= attribval2)]
    #st.dataframe(filtered_velocity, hide_index=True)
    return filtered_velocity
    
def filter_astronomical_unit(df, attribval1, attribval2):
    #st.write("Selected Astronomical Unit:", attribval1, "to", attribval2)
    # Filter the DataFrame based on the selected date range
    filtered_au = df[(df['astronomical'] >= attribval1) & (df['astronomical'] <= attribval2)]
    #st.dataframe(filtered_au, hide_index=True)
    return filtered_au

def filter_potentially_hazardous(df, attribval1):
    #st.write("Selected Potentially Hazardous:", attribval1)
    # Filter the DataFrame based on the selected date range
    filtered_hazardous = df[df['is_potentially_hazardous_asteroid'] == int(attribval1)]
    #st.dataframe(filtered_hazardous, hide_index=True)
    return filtered_hazardous
    

def filt_fn():
    col1, spacer, col2,spacer, col3 = st.columns([1, 0.5, 1, 0.5, 1])


    connection=db.connect(
        host="localhost",
        user="nasa",
        password="12345678",
        database="NASA_Asteroid",
        auth_plugin='mysql_native_password'
    )


    curr=connection.cursor()



    # to fetch the data from Asteroid table
    curr.execute("SELECT * FROM asteroids")
    data=curr.fetchall()

    df_asteroid=pd.DataFrame(data,columns=[i[0] for i in curr.description])


    # to fetch the data from Close_approach table

    curr.execute("SELECT * FROM close_approach")
    data1=curr.fetchall()

    df_closeapp=pd.DataFrame(data1,columns=[i[0] for i in curr.description])

    curr.close()
    connection.close()  
    
    # merging the two tables
    asteroid_closeapp_table =  pd.merge(df_asteroid, df_closeapp, how= 'left', left_on='id', right_on='neo_reference_id').drop_duplicates()
    #asteroid_closeapp_table = asteroid_closeapp_table.drop_duplicates(subset=['id'])

    # Slider 1: Min Magnitude
    with col1:
        min_magnitude = st.slider(
            "Min Magnitude",
            min_value=13.80,
            max_value=32.61,
            value=(13.80, 32.61),
            step=0.1
        )
        #st.write(f"Selected Min Magnitude: {type(min_magnitude)}")

    

    # Slider 2: Min Estimated Diameter(km)
    with col1:
        min_estimated_dia = st.slider(
            "Min Estimated Diameter(km)",
            min_value=0.00,
            max_value=4.62,
            value=(0.00, 4.62),
            step=0.1
        )
       # st.write(f"Selected Min Estimated Diameter(km): {min_estimated_dia}")

    # Slider 3: Max Estimated Diameter(km)
    with col1:
        max_estimated_dia = st.slider(
            "Max Estimated Diameter(km)",
            min_value=-0.00,
            max_value=10.33,
            value=(0.00, 10.33),
            step=0.1
        )
       # st.write(f"Selected Max Estimated Diameter(km): {max_estimated_dia}")

    # Slider 4: Relative Velocity (km/h) Range
    with col2:
        relative_velocity = st.slider(
            "Relative Velocity (km/h) Range",
            min_value=1418.21,
            max_value=173071.83,
            value=(1418.21, 173071.83),
            step=0.1
        )
        #st.write(f"Selected Relative Velocity (km/h) Range: {relative_velocity}")


    # Slider 5: Astronomical Unit
    with col2:
        astronomical_unit = st.slider(
            "Astronomical Unit", 0.00, 0.50, (0.00, 0.50), step=0.01 
        )
        #st.write(f"Selected Astronomical Unit: {astronomical_unit}")
        
       
       
        
    with col2:
        option1 = st.selectbox(
        "Only show potentially hazardous asteroids",
        ("0", "1")
        # 0 for No, 1 for Yes
        
        )

    #st.write("You selected:", option1)

    with col3:
        start_date = st.date_input("Start Date", dt(2024, 1, 1))
        
    with col3:
        end_date = st.date_input("End Date", dt(2024, 1, 8))
     
    submit_button = st.button("Filter", use_container_width=True)
    if submit_button:
       # st.write(len(asteroid_closeapp_table), "rows found")
        df_filtered = filtered_date(asteroid_closeapp_table, start_date, end_date) 
        #st.write(len(df_filtered), "rows found")
        df_filtered = filter_min_magnitude(df_filtered, min_magnitude[0], min_magnitude[1])
        df_filtered = filter_min_estimated_diameter(df_filtered, min_estimated_dia[0], min_estimated_dia[1])
        df_filtered = filter_max_estimated_diameter(df_filtered, max_estimated_dia[0], max_estimated_dia[1])
        df_filtered = filter_relative_velocity(df_filtered, relative_velocity[0], relative_velocity[1])
        df_filtered = filter_astronomical_unit(df_filtered, astronomical_unit[0], astronomical_unit[1])
        df_filtered = filter_potentially_hazardous(df_filtered, option1) 
        #st.write(len(df_filtered), "rows found")
        st.dataframe(df_filtered, hide_index=True)
        
   
# Content for each tab


if selected == "Filters":
    st.title("Filters ")
    filt_fn()
    
elif selected == "Queries":
    st.title("Select your Query")
    queries_fn()
    


