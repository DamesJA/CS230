"""
Name: Damian Amante
CS230: Section 2F
Data: NYC Vehicle Collisions
URL: https://share.streamlit.io/damesja/cs230/main/finalProject.py

Description:
 - The first thing I have in my program is a welcome statement
 - The second thing in my program is adding a function to choose color of the background. This I am proud of that I 
 figured out because I had to edit the html
 - I then created a map that shows the location of all the collisions (displayed with dots)
 - I then created a bar chart that shows the "persons injured" in different zip codes in NY
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import pydeck as pdk
import csv

name_of_file = 'NYC_vehicle_collisions_data.csv'
data = pd.read_csv(name_of_file, encoding="utf-8")
data.rename(columns=({'LATITUDE': 'latitude', 'LONGITUDE': 'longitude'}), inplace=True)


def welcome_statement():
    name = st.text_input("Enter your name:")
    experience = st.slider("On a scale of 1-10, what is your experience with streamlit:", min_value=1, max_value=10)
    message = ''
    if experience <= 3:
        message += 'I see you are not the most experienced, but it seems as though you have some knowledge of streamlit'
    elif experience <= 6:
        message += 'You definitely have some experience but are not 100% of the way there to mastering streamlit just yet'
    else:
        message += 'You are probably very advanced at streamlit and have been working with it for several years'
    st.write(f'Hi {name}, {message}')


def choose_color(colors_dict, color):
    color_code = colors_dict[color]
    return color_code


# this function chooses the background color and implements it into the code
def choose_background_color():
    # SOMETHING COOL THAT I MADE! I edited the the style using css and python (proud of it because I figured it out on my own)
    colors = {'brown': '#964B00', 'green': '#00bd00', 'darkpink': '#E75480', 'cobalt': '#0047ab'}
    colors_list = list(colors.keys())
    color = st.sidebar.radio('background colors', colors_list)
    color_selection = choose_color(colors, color)
    st.markdown(
        f"""
        <style>
            .reportview-container {{
                background-color: {color_selection};
            }}
        </style>
        """,
        unsafe_allow_html=True
    )


# This function creates the map that is in the data
def map_query():
    vehicle_1_types = list(dict.fromkeys(data['VEHICLE 1 TYPE'].dropna()))
    vehicle_1_type = st.selectbox('vehicle type', vehicle_1_types)
    dfv = data[(data['VEHICLE 1 TYPE'] == vehicle_1_type) | (data['VEHICLE 2 TYPE'] == vehicle_1_type)]

    dfv_2 = dfv[['latitude', 'longitude']].dropna().copy()
    st.dataframe(dfv_2)

    st.title("Locations of Collision in New York")
    st.write("Simple Map:")
    st.map(dfv_2)
    st.write("Customized Map:")
    view_state = pdk.ViewState(
        latitude=dfv_2["latitude"].mean(),
        longitude=dfv_2["longitude"].mean(),
        zoom=10,
        pitch=0)
    #
    layer1 = pdk.Layer('ScatterplotLayer',
                       data=dfv_2,
                       get_position='[longitude, latitude]',
                       get_radius=100,
                       get_color=[0, 0, 255],
                       pickable=True
                       )

    # The tool tip that goes along with the graph
    tool_tip = {"html": "collision:<br/> <b>{longitude}, {latitude}</b> ",
                "style": {"backgroundColor": "steelblue",
                          "color": "white"}
                }

    map = pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state,
        # mapbox_key=MAPKEY,
        layers=[layer1],
        tooltip=tool_tip
    )
    st.pydeck_chart(map)


# this function creates the bar chart
def barchart_query():
    persons_death_count_by_zip = {}
    with open(name_of_file, mode='r') as csv_file:
        zipcode_data = csv.DictReader(csv_file)
        for row in zipcode_data:
            zipcode = row['ZIP CODE']
            injured_num = row['PERSONS INJURED']
            if zipcode != 0:
                if zipcode not in persons_death_count_by_zip.keys():
                    persons_death_count_by_zip[zipcode] = eval(injured_num)
                else:
                    persons_death_count_by_zip[zipcode] += eval(injured_num)

    # making a list of all the zip codes in int form
    zipcodes_int_form = []
    for zipcode in list(data['ZIP CODE'].dropna()):
        zipcodes_int_form.append(int(zipcode))
    # these sliders allow the user to choose options where they can choose which zipcodes they want to show
    zip1 = st.sidebar.selectbox('Zip Code 1', zipcodes_int_form)
    zip2 = st.sidebar.selectbox('Zip Code 2', zipcodes_int_form)
    zip3 = st.sidebar.selectbox('Zip Code 3', zipcodes_int_form)
    x = [zip1, zip2, zip3]
    y = [persons_death_count_by_zip[str(zip1)], persons_death_count_by_zip[str(zip2)],
         persons_death_count_by_zip[str(zip3)]]

    fig, ax = plt.subplots()
    ax.yaxis.grid(linestyle='dashed', zorder=0)
    ax.bar(x, y, color=['black', 'red', 'green'])
    ax.set_title("injured by zipcode")
    ax.set_xlabel('Zipcodes')
    ax.set_ylabel('Injured_Num')
    st.write(fig)


# this is the main function that starts the execution of the program
def main():
    choose_background_color()
    welcome_statement()
    map_query()
    barchart_query()


main()
