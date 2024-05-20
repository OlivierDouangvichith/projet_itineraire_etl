import requests


def trouver_etablissement_sur_tripadvisor(nom_etablissement, latitude, longitude):
    # Clé API de TripAdvisor
    API_KEY = "A53D361A3E26481FA50F307F80E866F4"

    # URL de l'API de TripAdvisor pour la recherche d'établissements
    search_url = "https://api.content.tripadvisor.com/api/v1/location/search"

    # Paramètres de la requête
    params = {
        "key": API_KEY,
        "searchQuery": nom_etablissement,
        "latLong": "{},{}".format(latitude, longitude),
        "radius": 1,
        "language": "en"
    }

    try:
        # Envoie de la requête à l'API de TripAdvisor
        response = requests.get(search_url, params=params)

        # Vérifie si la requête a réussi
        if response.status_code == 200:
            data = response.json()
            # Récupère le premier établissement trouvé
            etablissement = data.get('data', [])
            if etablissement:
                return etablissement[0]
            else:
                print("Aucun établissement trouvé sur TripAdvisor.")
                return None
        else:
            # Affiche un message d'erreur si la requête a échoué
            print("Erreur lors de la requête à l'API TripAdvisor. Statut :", response.status_code)
            return None
    except Exception as e:
        # Affiche un message d'erreur en cas d'exception
        print("Erreur :", e)
        return None


def recuperer_avis_etablissement(location_id):
    # Clé API de TripAdvisor
    API_KEY = "A53D361A3E26481FA50F307F80E866F4"

    # URL de l'API de TripAdvisor pour récupérer les avis de l'établissement
    reviews_url = f"https://api.content.tripadvisor.com/api/v1/location/{location_id}/reviews"

    # Paramètres de la requête pour récupérer les avis
    params = {
        "key": API_KEY,
        "language": "en"
    }

    try:
        # Envoie de la requête à l'API de TripAdvisor pour récupérer les avis
        response = requests.get(reviews_url, params=params)

        # Vérifie si la requête a réussi
        if response.status_code == 200:
            data = response.json()
            rating = data['data'][0]['rating']
            return rating
        else:
            # Affiche un message d'erreur si la requête a échoué
            print("Erreur lors de la requête pour récupérer les avis. Statut :", response.status_code)
            return None
    except Exception as e:
        # Affiche un message d'erreur en cas d'exception
        print("Erreur lors de la récupération des avis de l'établissement :", e)
        return None

# Exemple d'utilisation de la fonction
nom_etablissement = "l'auberge du gros"
latitude = 49.1135  # Latitude de l'établissement
longitude = 6.3513  # Longitude de l'établissement

etablissement_trouve = trouver_etablissement_sur_tripadvisor(nom_etablissement, latitude, longitude)

if etablissement_trouve:
    print("Établissement trouvé sur TripAdvisor :", etablissement_trouve.get('location_id'))
    print("Nom de l'établissement trouvé sur TripAdvisor :", etablissement_trouve.get('name'))

    # Utilisation de l'ID de l'établissement pour récupérer des avis
    location_id = etablissement_trouve.get('location_id')

    avis_etablissement = recuperer_avis_etablissement(location_id)

    if avis_etablissement:
        print("Note de l'établissement :", avis_etablissement)
    else:
        print("Aucun avis trouvé sur TripAdvisor pour cet établissement.")
else:
    print("Aucun établissement trouvé sur TripAdvisor.")
