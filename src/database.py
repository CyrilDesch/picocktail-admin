import streamlit as st
import pandas as pd
from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError

##############################
## BASIC DATABASE FUNCTIONS ##
##############################

class Database:
  _instance = None
  @staticmethod
  def get_instance():
    if Database._instance is None:
      Database()
    return Database._instance

  def __init__(self):
    if Database._instance is not None:
      raise Exception("This class is a singleton !")
    else:
      Database._instance = self
      self.dbConnection = st.connection('mysql', type='sql')


# Execute INSERT / UPDATE / DELETE SQL request
# Return True if query is ok !
def executeSQL(query, params={}):
  db = Database.get_instance().dbConnection
  with db.session as session:
    try:
      session.execute(text(query), params=params)
      session.commit()
      return True
    except SQLAlchemyError as e:
      session.rollback()
      return False



################################
## Dataframe to SQL functions ##
################################

# Update from difference of rows between two dataframes
# Args :
# - dataframe : Dataframe
# - originalDataframe : comparaison Dataframe
# - tableName : SQL Table name where update rows
# Return an error counter
# (Bad pratice but lack of time)
def updateRowsAsSQL(dataframe: pd.DataFrame, originalDataframe: pd.DataFrame, tableName):
  updates = dataframe.compare(originalDataframe)
  errorCount = 0

  for index, row in updates.iterrows():
    updateQuery = f"UPDATE {tableName} SET "
    updateQuery += ", ".join([f"{col} = :{col}" for col in row.index.levels[0]])
    updateQuery += " WHERE id = :id;"
    
    params = {col: row[(col, "self")] for col in row.index.levels[0]}
    params['id'] = index
    errorCount += 0 if executeSQL(updateQuery, params) else 1

  return errorCount


# Insert rows from a dataframe
# Args :
# - dataframe : Dataframe
# - tableName : SQL Table name where insert rows
# Return an error counter
# (Bad pratice but lack of time)
def insertRowsAsSQL(dataframe: pd.DataFrame, tableName):
  errorCount = 0

  for _, row in dataframe.iterrows():
    # Insert
    insertQuery = f"INSERT INTO {tableName} ({", ".join([f"{col}" for col in row.index])}) VALUES ("
    insertQuery += ", ".join([f":{col}" for col in row.index])
    insertQuery += ");"
    print(insertQuery)
    
    params = {col: row[col] for col in row.index}
    errorCount += 0 if executeSQL(insertQuery, params) else 1
    
  return errorCount


# Delete rows from a dataframe with rows number
# Args :
# - dataframe : Dataframe
# - indexList : List of row number to remove
# - tableName : SQL Table name where remove rows
# Return an error counter
# (Bad pratice but lack of time)
def deleteRowsAsSQL(dataframe: pd.DataFrame, rowsNumberList, tableName):
  errorCount = 0

  for rowNumber in rowsNumberList:
    deleteQuery = f"DELETE FROM {tableName} WHERE id = :id;"
    params = {'id': dataframe.iloc[rowNumber].name}
    errorCount += 0 if executeSQL(deleteQuery, params) else 1
    
  return errorCount
