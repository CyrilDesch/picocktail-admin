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

    users_df = db.query("SELECT * FROM users;", ttl=0)

    st.title('Utilisateurs')
    st.dataframe(users_df, column_config={"id": "ID", "cardUID": "Numéro de carte", "username": "Pseudo", "created_at": "Crée le"}, hide_index=True)

    return None


if __name__ == '__main__':
    main()