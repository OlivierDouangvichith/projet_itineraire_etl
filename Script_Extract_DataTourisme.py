import json
import os
import pandas as pd
import psycopg2
from psycopg2 import sql
from tqdm import tqdm

# Paramètres de la base de données
db_params = {
    'host': '188.166.105.53',
    'port': 65001,
    'database': 'postgres',
    'user': 'postgres',
    'password': 'LearnPostgreSQL'
}

# Chemin du fichier index.json
index_file_path = "index.json"

# Lecture du fichier index.json
with open(index_file_path, 'r', encoding='utf-8') as index_file:
    index_data = json.load(index_file)

# Liste pour stocker les données à insérer dans la base de données
table_data = []

for file_info in tqdm(index_data):
    file_path = os.path.join(os.path.dirname(index_file_path), "objects", file_info['file'])

    with open(file_path, 'r', encoding='utf-8', errors='replace') as json_file:
        json_data = json.load(json_file)

        label_fr = json_data.get('rdfs:label', {}).get('fr', [''])[0]

        # Vérifier si la liste 'hasDescription' est non vide avant d'essayer d'accéder à l'élément [0]
        description_fr_list = json_data.get('hasDescription', [])

        # Rechercher la description en français dans la liste
        description_fr = ''
        for desc_item in description_fr_list:
            if 'fr' in desc_item.get('@language', ''):
                description_fr = desc_item.get('@value', '')
                break

        telephone = json_data.get('hasContact', [{}])[0].get('schema:telephone', [''])[0]

        location_info = json_data.get('isLocatedAt', [{}])[0]
        address_info = location_info.get('schema:address', [{}])[0]
        address_locality = address_info.get('schema:addressLocality', '')

        geo_info = location_info.get('schema:geo', {})
        latitude = geo_info.get('schema:latitude', '')
        longitude = geo_info.get('schema:longitude', '')

        table_data.append({
            'Label (fr)': label_fr,
            'Description (fr)': description_fr,
            'Téléphone': telephone,
            'Adresse': address_info.get('schema:streetAddress', ''),
            'Ville': address_locality,
            'Latitude': latitude,
            'Longitude': longitude,
        })
        
