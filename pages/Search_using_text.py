import streamlit as st
from datetime import datetime, date
import module
from st_utils import display_images


def main()-> None:

    st.title("Search using text")

    default_start_date = datetime(1970, 1, 2)
    default_end_date = datetime.today()
    
    text_query = st.text_input("Enter a textual description")

    k = st.slider("Show top k results", min_value=1, max_value=10)

    start_date = st.date_input("Start Date", value=default_start_date, min_value=date(1970, 1, 1), max_value=date.today()).strftime("%Y-%m-%d")
    end_date = st.date_input("End Date", value=default_end_date, min_value=date(1970, 1, 1), max_value=date.today()).strftime("%Y-%m-%d")

    click = st.button("Search")

    if click:
        response = module.text_query(text_query, start_date, end_date, k)
        display_images(response)

    if st.button("Search using image instead"):
        st.switch_page("pages/Search_using_image.py")
    
    if st.button("Home"):
        st.switch_page("Home.py")

if __name__ == "__main__":
    main()