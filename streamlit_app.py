# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col , when_matched

# Write directly to the app
st.title('My Parents New Healthy Diner')
st.write('Breakfast Menu')
st.text('Breakfast Menu')
