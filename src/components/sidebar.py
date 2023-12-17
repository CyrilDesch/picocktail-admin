import streamlit as st
from helpers import img_to_bytes

def sidebar():

    st.sidebar.markdown('''<br />[<img src='data:image/png;base64,{}' class='img-fluid' width=150 height=150>](https://streamlit.io/)'''.format(img_to_bytes("logo-picocktail.png")), unsafe_allow_html=True)
    st.sidebar.header('Picock-tail dashboard')

    st.sidebar.markdown('''
    <small>Statistiques de la machine et création de recettes.</small>
    ''', unsafe_allow_html=True)

    return None