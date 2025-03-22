# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col , when_matched

# Write directly to the app
st.title(":cup_with_straw: My Parents New Healthy Diner :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

Name_on_order = st.text_input("Name on Smoothie:")
st.write("Name on your smoothie will be:", Name_on_order)

#session = get_active_session()
cnx=st.connection("snowflake")
session=cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "choose up to 5 ingredients:",my_dataframe,max_selections=5
)

if ingredients_list :
    ingredients_string=''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + Name_on_order + """')"""

#    st.write(my_insert_stmt)
#    st.stop()
    
    time_to_insert=st.button('Submit Order')

    if(time_to_insert):
        session.sql(my_insert_stmt).collect()
        st.success('Your smoothie is ordered, '+ Name_on_order+"!",icon="✅")
#        st.write("Your smoothie is ordered,",Name_on_order,"!")   

#if ingredients_string:
#    session.sql(my_insert_stmt).collect()
#    st.success('Your Smoothie is ordered!', icon="✅")
