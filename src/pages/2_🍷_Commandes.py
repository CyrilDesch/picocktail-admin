import streamlit as st
from database import Database
from components.sidebar import sidebar
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Initial page config
st.set_page_config(
    page_title='Commandes - Picock-tail',
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

    ## Récupération des données
    orders_df = db.query("SELECT * FROM orders;", ttl=0)
    recipes_df = db.query("SELECT * FROM recipes;", ttl=0)
    users_df = db.query("SELECT * FROM users;", ttl=0)


    #################################
    ## Transformations des données ##
    #################################

    # Mapping
    orders_df['created_at'] = pd.to_datetime(orders_df['created_at'])

    # Calcul du temps écoulé entre les commandes successives
    orders_df['previous_order_time'] = orders_df.groupby('user_id')['created_at'].shift()
    orders_df['time_between_orders'] = (orders_df['created_at'] - orders_df['previous_order_time']).dt.total_seconds() / 3600

    # Nettoyage: suppression des valeurs NaN et infinies (première commande de chaque utilisateur)
    orders_df = orders_df.dropna(subset=['time_between_orders'])

    # Jointure avec users_df et recipes_df pour obtenir les noms
    orders_df = orders_df.merge(users_df, left_on='user_id', right_on='id', how='left')
    orders_df = orders_df.merge(recipes_df, left_on='recipe_id', right_on='id', how='left')

    # Remplacer les IDs par des noms pour les recettes
    recipes_dict = recipes_df.set_index('id')['name'].to_dict()
    orders_with_names = orders_df.replace({'recipe_id': recipes_dict})

    # Remplacer les IDs par des noms pour les utilisateurs
    users_dict = users_df.set_index('id')['username'].to_dict()
    orders_with_names = orders_with_names.replace({'user_id': users_dict})


    ###############
    ## Affichage ##
    ###############


    st.markdown(f"# Détails des commandes <sub style='white-space: nowrap;'>- Total : {orders_with_names.size}</sub>", unsafe_allow_html=True)
    st.dataframe(orders_with_names[["id_x", "quantity", "recipe_id", "user_id", "created_at_x"]],
                hide_index=True,
                column_config={"id_x": "ID", "quantity": "Quantité", "recipe_id": "Recette", "user_id": "Utilisateur", "created_at_x": "Date de commande"})

    st.divider()

    # 1. Top Recettes Commandées - Pie Chart
    col1, col2, col3 = st.columns([8, 1, 1]) 
    with col1:
        top_recipes_named = orders_with_names.groupby('recipe_id').size()
        st.title("Répartition des recettes commandées :")  # Titre
        fig, ax = plt.subplots()
        ax.pie(top_recipes_named, labels=top_recipes_named.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig)

    st.divider()

    # 2. Consommation moyenne par utilisateur
    col1, col2, col3 = st.columns([8, 1, 1]) 
    with col1:
        avg_consumption_per_user_named = orders_with_names.groupby('user_id')['quantity'].mean()
        st.title("Quantité moyenne de consommation par utilisateur :")  # Titre
        st.bar_chart(avg_consumption_per_user_named)

    st.divider()

    # 3. Distribution des Commandes par Quantité
    st.title("Répartition des quantités commandées :")  # Titre
    col1, col2, col3 = st.columns([8, 1, 1]) 
    with col1:
        plt.figure(figsize=(10, 6))
        sns.boxplot(orders_with_names['quantity'])
        st.pyplot(plt)


    return None


if __name__ == '__main__':
    main()