import json
import psycopg2

# Paramètres de la base de données
db_params = {
    'host': '188.166.105.53',
    'port': 65001,
    'database': 'postgres',
    'user': 'postgres',
    'password': 'LearnPostgreSQL'
}

# Initialiser le dictionnaire pour stocker les sous-classes et leurs classes correspondantes
subclasses = {}

# Charger le fichier JSON-LD en spécifiant l'encodage UTF-8
with open('ontology.jsonld', 'r', encoding='utf-8') as file:
    data = json.load(file)

    # Rechercher tous les éléments qui ont une sous-classe et une classe correspondante
    for item in data:
        if '@type' in item and 'http://www.w3.org/2000/01/rdf-schema#subClassOf' in item:
            subclass_id = item['@id']
            superclass_id = item['http://www.w3.org/2000/01/rdf-schema#subClassOf'][0]['@id']

            # Extraire les noms des classes à partir des ID
            subclass_name = subclass_id.split('#')[-1]
            superclass_name = superclass_id.split('#')[-1]

            # Supprimer la partie 'http://schema.org/' de la valeur si elle est présente
            superclass_name = superclass_name.replace('http://schema.org/', '')

            # Ajouter la sous-classe et sa classe correspondante au dictionnaire
            subclasses[subclass_name] = superclass_name

# Connexion à la base de données
conn = psycopg2.connect(**db_params)
cur = conn.cursor()

# Création de la table types_de_poi si elle n'existe pas
cur.execute("CREATE TABLE IF NOT EXISTS types_de_poi (id SERIAL PRIMARY KEY, classe VARCHAR, superclasse VARCHAR)")

# Insertion des données dans la table
for subclass, superclass in subclasses.items():
    cur.execute("INSERT INTO types_de_poi (classe, superclasse) VALUES (%s, %s)", (subclass, superclass))

# Commit des modifications et fermeture de la connexion
conn.commit()
conn.close()

print("Données insérées avec succès dans la base de données.")
