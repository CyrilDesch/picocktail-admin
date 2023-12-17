import streamlit as st
from components.sidebar import sidebar

# Initial page config
st.set_page_config(
    page_title='Dashboard - Picock-tail',
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon = 'logo-picocktail.png'
)

def main():
    sidebar()
    body()
    return None

def body():
    st.markdown("""
    # Bienvenue sur le dashboard admin de Picock-tail
    
    🚀 **Lancez-vous dans la création de cocktail !** Avec cet espace, l'art de concocter des recettes innovantes est à portée de main. 🍹

    📊 **Plongez dans un océan de données !** Explorez des analyses détaillées et des statistiques fascinantes pour comprendre chaque aspect de la machine.
    """)
    return None

if __name__ == '__main__':
    main()