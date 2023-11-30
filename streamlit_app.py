import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Get data for fruit smoothie ingredients and set index to the fruit name
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
# Added two defaults to show users how to use the fruit picker :)
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# Fruityvice API call function
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    # Use pandas to normalise the fruityvice response and format
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    # Return data from function
    return fruityvice_normalized
    
# Display fruityvice stuff
streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("please select a fruit to get info")
    else:
        # Call function on fruit
        back_from_function = get_fruityvice_data(fruit_choice)
        # Display choice
        streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()

# New snowflake connector
streamlit.header("The fruit load list contains:")
# Snowflake function
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()

if streamlit.button('Get fruit load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.executite("insert into fruit_load_list values('from streamlit')")
        return "thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add to the list?')
if streamlit.button('Add a Fruit to the list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)

#streamlit.write('Thanks for adding:', add_my_fruit)
#my_cur.execuite("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('test from streamlit')")
