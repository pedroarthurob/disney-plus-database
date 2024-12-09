import sqlite3
import pandas as pd

con = sqlite3.connect("DisneyPlusCatalog.db")
cur = con.cursor()

arquivo_excel = "DisneyPlus.xlsx"
df = pd.read_excel(arquivo_excel)

# Função auxiliar para inserir dados com múltiplos valores
def insert_multi_values(con, data, table_name, unique_column, link_table, media_column, link_column):
    unique_values = set()
    link_data = []

    for media_id, items in data.items():
        if pd.isnull(items):
            continue
        for item in map(str.strip, items.split(',')):
            unique_values.add(item)
            link_data.append((media_id, item))

    # Inserir valores únicos na tabela principal
    unique_df = pd.DataFrame(unique_values, columns=[unique_column])
    unique_df.to_sql(table_name, con, if_exists="append", index=False)

    # Criar mapeamento
    value_map = pd.read_sql(f"SELECT ID, {unique_column} FROM {table_name}", con).set_index(unique_column)["ID"].to_dict()

    # Inserir na tabela de relacionamento
    link_df = pd.DataFrame(link_data, columns=[media_column, unique_column])
    link_df[link_column] = link_df[unique_column].map(value_map)
    link_df = link_df[[media_column, link_column]].drop_duplicates()
    link_df.to_sql(link_table, con, if_exists="append", index=False)

type_data = df['type'].dropna().drop_duplicates().reset_index(drop=True)
type_data.to_frame(name="Name").to_sql("Type", con, if_exists="append", index=False)

type_map = pd.read_sql("SELECT ID, Name FROM Type", con).set_index("Name")["ID"].to_dict()

# Inserir dados na tabela `Media`
df['TypeID'] = df['type'].map(type_map)
media_data = df[['show_id', 'TypeID', 'title', 'date_added', 'release_year', 'rating', 'duration', 'description']]
media_data.columns = ['ID', 'TypeID', 'Title', 'Date_Added', 'Release_Year', 'Rating', 'Duration', 'Description']
media_data.to_sql("Media", con, if_exists="append", index=False)

# Inserir dados em `Director` e `Cast`
insert_multi_values(con, df.set_index('show_id')['director'], "Person", "Name", "Director", "MediaID", "PersonID")
insert_multi_values(con, df.set_index('show_id')['cast'], "Person", "Name", "Cast", "MediaID", "PersonID")

# Inserir dados em `Country` e `MediaCountry`
insert_multi_values(con, df.set_index('show_id')['country'], "Country", "Name", "MediaCountry", "MediaID", "CountryID")

# Inserir dados em `Genre` e `MediaGenre`
insert_multi_values(con, df.set_index('show_id')['listed_in'], "Genre", "Name", "MediaGenre", "MediaID", "GenreID")

# Fechar conexão
con.close()
