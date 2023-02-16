import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title('My Mom\'s New Healthy Diner')
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-boiled Free-range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
streamlit.dataframe(my_fruit_list) 
 
#Pick list
fruits_selected = streamlit.multiselect('Pick some fruits:',
 list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
 fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
 #streamlit.text(fruityvice_response.json())
 # Normalise the json version
 fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
 return fruityvice_normalized
streamlit.header("Fruityvice Fruit Advice!")
try:
 fruit_choice = streamlit.text_input('What fruit would you like information about?')
 if not fruit_choice:
   streamlit.error('Please select a fruit to get information.')
  else:
   # output screen as table
   back_from_function = get_fruityvice_data(fruit_choice)
   streamlit.dataframe(back_from_function)
except URLError as e:
        streamlit.error()
 streamlit.header("View Our Fruit List -  Add Your Favourites!")
#Snowflake related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
        return my_cur.fetchall()
#Add a button to load the fruit
if streamlit.button('Get Fruit List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)
                                
   def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("Insert into pc_rivery_db.public.fruit_load_list
                       values ('"+new_fruit+"')")
        return "Thanks for adding " + new_fruit
#Allowing end user to a fruit to list
add_my_fruit = streamlit.text_input('What fruit do you like to add?')
#streamlit.write('Thanks for adding', add_my_fruit)
#my_cur.execute('Insert into fruit_load_list values ('from streamlit')')
if streamlit.button("Add a Fruit to the List"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_fromm_function = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)
