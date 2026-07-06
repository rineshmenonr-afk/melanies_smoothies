# Import python packages
import streamlit as st

from snowflake.snowpark.functions import col



# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """ Choose the fruits you want in your custom Smoothie !
  """
)


cnx = st.connection("snowflake")
session = cnx. session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)

nameoftheorder = st.text_input('Name on Smoothie')
st.write('The Name on the smoothies will be  ', nameoftheorder)




ingredients_list = st.multiselect(
'Choose up to 5 ingredients:'
,my_dataframe , max_selections = 5)

st.write(ingredients_list)
st.text(ingredients_list)



if ingredients_list:

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    submit = st.button("Submit Order")

    if submit:

        my_insert_stmt = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS
        (INGREDIENTS, NAME_ON_ORDER)
        VALUES ('{ingredients_string}', '{nameoftheorder}')
        """

        session.sql(my_insert_stmt).collect()

        st.success(f"Your Smoothie is ordered, {nameoftheorder}!", icon="✅")
        
        
        
import requests  
smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
st.text(smoothiefroot_response)

































