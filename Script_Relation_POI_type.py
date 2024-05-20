import psycopg2

# Paramètres de la base de données
db_params = {
    'host': '188.166.105.53',
    'port': 65001,
    'database': 'postgres',
    'user': 'postgres',
    'password': 'LearnPostgreSQL'
}

# Connexion à la base de données
conn = psycopg2.connect(**db_params)
cur = conn.cursor()

# Requête pour sélectionner les 10 premières lignes de la table datatourisme
cur.execute("SELECT id, type FROM datatourisme10 LIMIT 10")

# Récupération des résultats
rows = cur.fetchall()

# Parcours des résultats
for row in rows:
    id_datatourisme, types = row

    # Séparation des types par des virgules
    types_list = [t.strip() for t in types.split(',')]

    # Vérification pour chaque type
    for t in types_list:
        # Recherche du type dans la table types_de_poi
        cur.execute("SELECT id, classe FROM types_de_poi WHERE classe = %s", (t,))
        result = cur.fetchone()

        # Si le type est trouvé
        if result:
            id_type_de_poi, classe = result

            # Insertion dans la table de liaison many-to-many
            cur.execute(
                "INSERT INTO liaison_datatourisme_types_de_poi (id_datatourisme, id_type_de_poi) VALUES (%s, %s)",
                (id_datatourisme, id_type_de_poi))

# Commit des modifications et fermeture de la connexion
conn.commit()
conn.close()
