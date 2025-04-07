import requests

# Configuration
es_url = "http://localhost:9200/logs/_doc"
log_file = "logs.txt"

# Ouvrir le fichier de logs et lire chaque ligne
with open(log_file, "r") as file:
    for line in file:
        # Préparer les données en JSON
        data = {
            "message": line.strip()
        }
        try:
            # Envoyer la requête POST à ElasticSearch
            response = requests.post(es_url, json=data)
            # Vérifier la réponse
            if response.status_code == 201:
                print(f"Log ajouté avec succès: {line.strip()}")
            else:
                print(f"Erreur {response.status_code}: {response.json()}")
        except Exception as e:
            print(f"Erreur lors de l'envoi du log: {e}")
