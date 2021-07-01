"""
Name: Damian Amante
CS230: Section 2F
Data: NYC vehicle Collisions
URL:

Description:
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import pydeck as pdk

data = pd.read_csv('NYC_vehicle_collisions_data.csv', encoding="utf-8")
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

def choose_background_color():
    # SOMETHING COOL THAT I MADE!
    colors = {'green': '#00bd00', 'darkpink': '#E75480', 'brown': '#964B00', 'cobalt': '#0047ab'}
    colors_list = list(colors.keys())
    color = st.sidebar.radio('background colors', colors_list)
    color_selection = colors[color]
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


# taking out all rows that don't have a proper longitude and latitude
# for i in range(0, len(data)):
#     if type(data['longitude']) != float:


# def query_1():
#     # array with all the street names with no duplicates
#     street_names = list(dict.fromkeys(data['ON STREET NAME']))
#     for i in range(0, len(street_names) - 1):
#         # taking out the street names that are nan
#         if type(street_names[i]) == float:
#             street_names.pop(i)
#     # print(street_names)
#
#     months = []
#     years = []
#     for i in range(0, len(data)):
#         if int(data['DATE'][i].split('/')[0]) not in months:
#             months.append(int(data['DATE'][i].split('/')[0]))
#         if int(data['DATE'][i].split('/')[2]) not in years:
#             years.append(int(data['DATE'][i].split('/')[2]))
#     # print(months)
#     # print(years)
#
#     street_selection = st.selectbox('Select a street name', street_names)
#     month_selection = st.slider('Select a month', min(months), max(months), 1)
#     year_selection = st.slider('Select a year', min(years), max(years))
#
#     # selected_df = data[data['ON STREET NAME'] == street_selection and data['DATE'].split('/')[0] == month_selection and data['DATE'].split('/')[2] == year_selection]
#     selected_df_1 = data[data['ON STREET NAME'] == street_selection]
#     selected_df_2 = selected_df_1[data['PERSONS INJURED'] >= 1]
#     print(selected_df_2)
#
#     # and data['PEDESTRIANS INJURED'] >= 1 and data['CYCLISTS INJURED'] >= 1 and data['PERSONS INJURED'] >= 1
#
#     # selected_df_2 = selected_df_1[selected_df_1['DATE'].str.split('/')[0] == month_selection]
#     # selected_df_3 = selected_df_2[selected_df_2['DATE'].str.split('/')[2] == year_selection]
#
#     # and data['Month'] == data[month_selection] and data['Year'] == data[year_selection]
#     # print(selected_df)
#
#     dictionary = {'PERSONS INJURED': sum(selected_df_1['PERSONS INJURED']),
#                   'PEDESTRIANS INJURED': sum(selected_df_1['PEDESTRIANS INJURED']),
#                   'CYCLISTS INJURED': sum(selected_df_1['CYCLISTS INJURED']),
#                   'MOTORISTS INJURED': sum(selected_df_1['PERSONS INJURED'])}
#
#     fig, ax = plt.subplots()
#     ax.bar(dictionary.keys(), dictionary.values())
#     # plt.xlabel('amount of pepo')
#     # plt.ylabel(f'log of sum')
# #     ax.legend([injured], [killed], loc=9)
#     st.pyplot(fig)
def barchart():
    pass
#     bar_df = data[['ZIP CODE', 'PERSONS INJURED']].dropna().groupby('ZIP CODE').count('PERSONS INJURED')
#     print(bar_df)
    # colors = {"red": "r", "green": "g", "yellow": "y", "blue": "b", "cyan": "c"}
    # color_names = list(colors.keys())
    #
    # def bar(values, color1=colors["cyan"]):
    #     p = values
    #     x = range(4)
    #     plt.bar(x, p, color=color1)
    #     return plt
    #
    # st.title('Bar Chart')
    # st.sidebar.header('Inputs')
    #
    # value1 = st.sidebar.slider("Value 1", 1, 50)
    # value2 = st.sidebar.slider("Value 2", 1, 50)
    # value3 = st.sidebar.slider("Value 3", 1, 50)
    # value4 = st.sidebar.slider("Value 4", 1, 50)
    #
    # values = [value1, value2, value3, value4]
    #
    # color1 = st.sidebar.radio('Color:', color_names)
    #
    # st.pyplot(bar(values, colors[color1]))
    # st.sidebar.table(values)
    # if st.sidebar.button("Press Me"):
    #     st.balloons()


def query_1():
    vehicle_1_types = list(dict.fromkeys(data['VEHICLE 1 TYPE'].dropna()))
    vehicle_1_type = st.selectbox('vehicle type', vehicle_1_types)
    dfv = data[(data['VEHICLE 1 TYPE'] == vehicle_1_type) | (data['VEHICLE 2 TYPE'] == vehicle_1_type)]

    dfv_2 = dfv[['latitude', 'longitude']].dropna().copy()
    st.dataframe(dfv_2)
    # print(dfv_2)

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


def main():
    choose_background_color()
    welcome_statement()
    barchart()
    query_1()


main()
