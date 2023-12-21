import streamlit as st
from database import Database, updateRowsAsSQL, insertRowsAsSQL, deleteRowsAsSQL
from components.sidebar import sidebar
import pandas as pd

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


# Streamlit and SQL when they are together are really big shit, 
# no logic in the management of data flows. 
# In short, this code will be complicated to understand due to problems.
def body():
    db = Database.get_instance().dbConnection
    recipesDf = db.query('SELECT * from recipes;', ttl=0)
    recipesDf = recipesDf.set_index("id")

    st.markdown("""
    # Gestion des recettes
    
    Vous pouvez **ajouter**, **modifier** et **supprimer** des recettes depuis cette interface.
    """)

    editedRecipesDf = st.data_editor(recipesDf, 
        key="editor",
        hide_index=True, 
        num_rows="dynamic", 
        column_order=["name", "description", "rate_bottle_one", "rate_bottle_two", "rate_bottle_three", "created_at"],
        column_config={"name": "Nom", "description": "Description", "rate_bottle_one": "Taux bouteille 1", "rate_bottle_two": "Taux bouteille 2", "rate_bottle_three": "Taux bouteille 3", "created_at": "Crée le"})
   
    # On button click
    if st.button(label="Sauvegarder", type="primary"):
        insertedAndDeletedRows = st.session_state["editor"]
        newRowsDf = pd.DataFrame(insertedAndDeletedRows["added_rows"])

        errorCounter = 0
        errorCounter += deleteRowsAsSQL(dataframe=recipesDf, rowsNumberList=insertedAndDeletedRows["deleted_rows"], tableName="recipes")
        
        insertedAndDeletedRows["deleted_rows"].sort(reverse=True)
        for row in insertedAndDeletedRows["deleted_rows"]:
            recipesDf = recipesDf.drop(recipesDf.iloc[row].name, axis=0)
        errorCounter += updateRowsAsSQL(originalDataframe=recipesDf, dataframe=editedRecipesDf, tableName="recipes")
        errorCounter += insertRowsAsSQL(dataframe=newRowsDf, tableName="recipes")

        if (errorCounter == 0):
            st.success("Base des recettes mise à jour !")
        else:
            st.error(f"{errorCounter} erreur(s) survenue(s) !")

    return None


if __name__ == '__main__':
    main()