import psycopg2
from psycopg2 import sql

# Paramètres de la base de données
db_params = {
    'host': '188.166.105.53',
    'port': 65001,
    'database': 'postgres',
    'user': 'postgres',
    'password': 'LearnPostgreSQL'
}

# Connexion à la base de données
print("Connexion à la base de données...")
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Création de la table DataTourisme5
print("Création de la table DataTourisme5...")
create_table_query = sql.SQL("""
    CREATE TABLE IF NOT EXISTS DataTourisme5 (
        id SERIAL PRIMARY KEY,
        label_fr VARCHAR(1000),
        description_fr TEXT,
        telephone VARCHAR(255),
        adresse VARCHAR(1000),
        ville VARCHAR(255),
        latitude VARCHAR(255),
        longitude VARCHAR(255)
    );
""")

cursor.execute(create_table_query)
print("Table DataTourisme5 créée avec succès.")

# Insertion des données dans la table
print("Insertion des données dans la table...")
insert_query = sql.SQL("""
    INSERT INTO DataTourisme5 (label_fr, description_fr, telephone, adresse, ville, latitude, longitude)
    VALUES (%(label_fr)s, %(description_fr)s, %(telephone)s, %(adresse)s, %(ville)s, %(latitude)s, %(longitude)s);
""")

batch_size = 100  # Taille du lot
total_records = len(table_data)
inserted_records = 0

try:
    for i in range(0, total_records, batch_size):
        batch_data = table_data[i:i+batch_size]
        for data in batch_data:
            label_fr = data['Label (fr)']
            description_fr = data['Description (fr)']
            telephone = data['Téléphone']
            adresse = data['Adresse']
            ville = data['Ville']
            latitude = data['Latitude']
            longitude = data['Longitude']

            cursor.execute(insert_query, {
                'label_fr': label_fr,
                'description_fr': description_fr,
                'telephone': telephone,
                'adresse': adresse,
                'ville': ville,
                'latitude': latitude,
                'longitude': longitude,
            })
            inserted_records += 1
            percentage_complete = (inserted_records / total_records) * 100
            print(f"Insertion en cours... {inserted_records}/{total_records} ({percentage_complete:.2f}%)", end="\r")
        conn.commit()
except Exception as e:
    conn.rollback()  # Annulation de toutes les opérations en attente en cas d'erreur
    print(f"Erreur lors de l'insertion des données : {e}")

# Fermeture de la connexion
print("\nFermeture de la connexion...")
cursor.close()
conn.close()

print("Connexion fermée.")
