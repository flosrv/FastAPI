import pandas as pd
from sqlalchemy import text

def create_table_in_mysql(df: pd.DataFrame, table_name: str, engine):
    # Vérifier si la table existe déjà
    check_table_sql = f"SHOW TABLES LIKE '{table_name}';"

    try:
        with engine.connect() as connection:
            result = connection.execute(text(check_table_sql))
            if result.fetchone():
                print(f"⚠️ La table '{table_name}' existe déjà dans MySQL.")
                return  # Ne pas recréer la table si elle existe déjà

            # Définition des colonnes
            column_definitions = []
            for column_name, dtype in df.dtypes.items():
                if dtype == 'object': 
                    column_type = "VARCHAR(255)"
                elif dtype == 'int64':  
                    column_type = "INT"
                elif dtype == 'float64': 
                    column_type = "FLOAT"
                elif dtype == 'datetime64[ns]': 
                    column_type = "DATETIME"
                elif dtype == 'datetime64[ns, UTC]': 
                    column_type = "DATETIME"
                elif dtype == 'timedelta64[ns]':  
                    column_type = "TIME"
                elif dtype == 'bool':  
                    column_type = "BOOLEAN"
                elif dtype == 'time64[ns]': 
                    column_type = "TIME"
                else:
                    column_type = "VARCHAR(255)" 

                column_definitions.append(f"`{column_name}` {column_type}")

            # Création de la table
            create_table_sql = f"CREATE TABLE `{table_name}` ({', '.join(column_definitions)});"
            connection.execute(text(create_table_sql))
            print(f"✅ Table '{table_name}' créée avec succès dans MySQL.")

    except Exception as e:
        print(f"❌ Erreur lors de la création de la table : {e}")

def insert_new_rows(engine, df: pd.DataFrame, table_name: str):
    """
    Insère uniquement les nouvelles lignes de df dans MySQL en comparant la colonne 'Datetime'.
    """
    try:
        # Vérifier si la table existe et récupérer la valeur max de Datetime
        query = f"SELECT MAX(Datetime) FROM `{table_name}`;"
        with engine.connect() as connection:
            result = connection.execute(text(query)).scalar()  # Récupérer la valeur max
        
        # Si la table est vide, insérer tout le DataFrame
        if result is None:
            print(f"💾 Aucune donnée dans '{table_name}', insertion de toutes les lignes.")
            df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
            print(f"✅ {len(df)} nouvelles lignes insérées dans '{table_name}'.")
            return
        
        # Filtrer les nouvelles lignes (celles avec un Datetime plus grand que la valeur max en base)
        df["Datetime"] = pd.to_datetime(df["Datetime"])  # S'assurer que la colonne est bien en datetime
        new_rows = df[df["Datetime"] > result]

        if new_rows.empty:
            print(f"✅ Aucune nouvelle ligne à insérer dans '{table_name}'.")
            return

        # Insérer uniquement les nouvelles lignes
        new_rows.to_sql(name=table_name, con=engine, if_exists='append', index=False)
        print(f"✅ {len(new_rows)} nouvelles lignes insérées dans '{table_name}'.")

    except Exception as e:
        print(f"❌ Erreur lors de l'insertion des nouvelles lignes : {e}")

def convert_df_columns(df):
    """
    Convertit chaque colonne en son type approprié sans modifier les données
    ou introduire des NaN.
    
    Args:
    - df: pd.DataFrame. Le DataFrame à traiter.
    
    Returns:
    - pd.DataFrame: Le DataFrame avec les types de données convertis.
    """
    
    # Traitement des colonnes avec les types appropriés
    for col in df.columns:
        # Convertir les colonnes numériques
        if df[col].dtype == 'object':
            # Tenter de convertir en float si c'est un nombre représenté par des strings
            try:
                # Convertir en float pour les colonnes qui peuvent l'être (ex: "Wind Speed (km/h)", "Pressure (hPa)", etc.)
                df[col] = pd.to_numeric(df[col], errors='raise')
            except ValueError:
                # Si la conversion échoue, laisser la colonne intacte
                pass
                
        # Convertir des dates si la colonne contient des chaînes de caractères représentant des dates
        if df[col].dtype == 'object' and 'date' in col.lower():
            try:
                df[col] = pd.to_datetime(df[col], errors='raise')
            except ValueError:
                pass
        
        # Convertir les booléens (is_day) en int
        if col == "is_day":
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    # Assurer les types numériques pour les colonnes déjà numériques mais mal typées
    for col in df.select_dtypes(include=['float64', 'int64']).columns:
        df[col] = df[col].astype(pd.Float64Dtype())  # Garantir une gestion correcte des NaN dans les colonnes numériques

    return df








