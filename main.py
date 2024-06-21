import requests

def get_orcid_record(scopus_id, access_token):
    # Construire l'URL de l'API ORCID pour rechercher par ID Scopus
    search_url = f"https://pub.orcid.org/v3.0/search/?q=scopus-id:{scopus_id}"
    
    # Définir les en-têtes pour la requête
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    # Envoyer la requête de recherche à l'API ORCID
    response = requests.get(search_url, headers=headers)
    
    # Vérifier le statut de la réponse
    if response.status_code == 200:
        data = response.json()
        
        # Vérifier si des résultats ont été trouvés
        if 'result' in data and len(data['result']) > 0:
            # Extraire l'ORCID iD du premier résultat trouvé
            orcid_id = data['result'][0]['orcid-identifier']['path']
            
            # Construire l'URL pour récupérer le CV du chercheur
            cv_url = f"https://pub.orcid.org/v3.0/{orcid_id}/record"
            
            # Modifier les en-têtes pour accepter le XML
            headers['Accept'] = 'application/vnd.orcid+xml'
            
            # Envoyer la requête pour récupérer le CV
            cv_response = requests.get(cv_url, headers=headers)
            
            # Vérifier le statut de la réponse
            if cv_response.status_code == 200:
                cv_data = cv_response.text
                return cv_data
            else:
                return "Erreur lors de la récupération du CV"
        else:
            return "chercheur absent"
    else:
        return f"Erreur lors de la recherche : {response.status_code}"

# Exemple d'utilisation
scopus_id = "1234567890"
access_token = "votre_access_token_ici"
cv_data = get_orcid_record(scopus_id, access_token)

if "chercheur absent" not in cv_data and "Erreur" not in cv_data:
    print("CV du chercheur :", cv_data)
else:
    print(cv_data)
