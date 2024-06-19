import streamlit as st
import module
import os

def display_images(results):
    for i in results['matches']:
        st.image(os.path.join(module.dir, i['id']), caption = i['id'], width = 400)