import streamlit as st
import module
from st_utils import display_images
from datetime import datetime, date

def main()-> None:

    st.title("Search using image")

    default_start_date = datetime(1970, 1, 2)
    default_end_date = datetime.today()

    image_query = st.file_uploader("Choose a file", ['png', 'jpg','jpeg'])

    if image_query:
        st.image(image_query, caption=image_query.name, width = 200)

    k = st.slider("Show top k results", min_value=1, max_value=10)

    start_date = st.date_input("Start Date", value=default_start_date, min_value=date(1970, 1, 1), max_value=date.today()).strftime("%Y-%m-%d")
    end_date = st.date_input("End Date", value=default_end_date, min_value=date(1970, 1, 1), max_value=date.today()).strftime("%Y-%m-%d")

    click = st.button("Search")

    if click:
        response = module.image_query(image_query, start_date, end_date, k)
        display_images(response)

    if st.button("Search using text instead"):
        st.switch_page("pages/Search_using_text.py")

    if st.button("Home"):
        st.switch_page("Home.py")

if __name__ == "__main__":
    main()