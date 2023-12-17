import streamlit as st
from database import Database
from components.sidebar import sidebar

# Initial page config
st.set_page_config(
    page_title='Recettes - Picock-tail',
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon = 'logo-picocktail.png',
)

def main():
    sidebar()
    body()
    return None

def body():
    db = Database.get_instance().dbConnection

    # Initialize db connection
    df = db.query('SELECT * from recipes;', ttl=600)

    #st.dataframe(df)

    st.markdown("""
    # COUCOU les utilisateurs
    """)
    return None


if __name__ == '__main__':
    main()