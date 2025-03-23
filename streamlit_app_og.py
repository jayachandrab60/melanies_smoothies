# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col , when_matched
import requests
import pandas 

st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

Name_on_order = st.text_input("Name on Smoothie:")
st.write("Name on your smoothie will be:", Name_on_order)

cnx=st.connection("snowflake")
session=cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#convert the snowpark dataframe to a pandas dataframe so we can use LOC function
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)

ingredients_list = st.multiselect(
    "choose up to 5 ingredients:",my_dataframe,max_selections=5
)

if ingredients_list :
    ingredients_string=''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(fruit_chosen+ ' Nutrition Iformation ')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+ fruit_chosen)
        sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + Name_on_order + """')"""

    time_to_insert=st.button('Submit Order')

    if(time_to_insert):
        session.sql(my_insert_stmt).collect()
        st.success('Your smoothie is ordered, '+ Name_on_order+"!",icon="✅")



