# Import python packages
import streamlit as st
import requests

from snowflake.snowpark.functions import col

# Page Title
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Read the fruit table
my_dataframe = (
    session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS")
    .select(col("FRUIT_NAME"), col("SEARCH_ON"))
)

# Convert the Snowpark Dataframe to a Pa
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)


# Display available fruits
st.dataframe(my_dataframe, use_container_width=True)

# Customer name
nameoftheorder = st.text_input("Name on Smoothie")

st.write("The name on the smoothie will be:", nameoftheorder)

# Get the fruit names for the multiselect
fruit_options = [row["FRUIT_NAME"] for row in my_dataframe.collect()]

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_options,
    max_selections=5,
)

# Display selected fruits
st.write(ingredients_list)

ingredients_string = ""

# Display nutrition information
if ingredients_list:

    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ''
            
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
            # st.write('The search value for ', fruit_chosen, ' is ', search_on, '.')
            
        st.subheader (fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

        if smoothiefroot_response.status_code == 200:
            st.subheader(f"{fruit_chosen} Nutrition Information")
            st.json(smoothiefroot_response.json())
        else:
            st.error(f"Unable to retrieve data for {fruit_chosen}")

# Submit order
if st.button("Submit Order"):

    my_insert_stmt = f"""
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS
        (INGREDIENTS, NAME_ON_ORDER)
        VALUES ('{ingredients_string}', '{nameoftheorder}')
    """

    session.sql(my_insert_stmt).collect()

    st.success(f"Your Smoothie is ordered, {nameoftheorder}! ✅")
