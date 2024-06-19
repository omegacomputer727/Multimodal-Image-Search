import streamlit as st
import module
import multiprocessing


def main()-> None:

    st.title("Multimodal image search")

    st.divider()

    st.subheader("Choose the query modality:")
    if st.button("Search using text"):
        st.switch_page("pages/Search_using_text.py")

    if st.button("Search using image"):
        st.switch_page("pages/Search_using_image.py")


    st.subheader("Upload newly added files to the database in the backgroud")
    if st.button("Update/Refresh database"):
        process = multiprocessing.Process(target = module.upload)
        process.start()

    st.subheader("Clear contents of the database")
    if st.button("Clear database"):
        with st.spinner("Clearing database..."):
            module.delete()
        st.success("Database cleared successfully")
    
        
if __name__ == "__main__":
    main()