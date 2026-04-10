# Import python packages.
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app.
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """
  Choose the fruits you want in your custom Smoothie!
  """
)

# option = st.selectbox('What is your favourite fruit?',('Banana','Strawberries', 'Peaches'))
# st.write('You selected: ',option)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:',name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredient_list = st.multiselect(
    'Choose upto 5 ingredients'
    , my_dataframe
    , max_selections = 5
)

if ingredient_list:
    # st.write(ingredient_list)
    # st.text(ingredient_list)

    ingredient_string = ''

    for fruit_chosen in ingredient_list:
        ingredient_string = ingredient_string + ' ' + fruit_chosen

    insert_stmt = """
        insert into smoothies.public.orders(ingredients,name_on_order) 
        values ('"""+ingredient_string+"""','"""+name_on_order+"""')
    """

    # st.write(insert_stmt)
        
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(insert_stmt).collect()
        st.success('Your Smoothie is ordered!'+name_on_order, icon="✅")
