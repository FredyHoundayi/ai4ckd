Documentation de l'API AI4CKD
Description
API de prédiction des stades d'Insuffisance Rénale Chronique (IRC) utilisant un modèle XGBoost entraîné. L'API prend en entrée des paramètres cliniques et retourne le stade prédit (1 à 5) avec un score de confiance.

Endpoints
POST /predict
Prédit le stade de l'IRC (1 à 5) à partir des données cliniques.

Requête
Content-Type: application/json

Body (exemple) :

json
Copy
{
  "creatinine": 99.89,
  "ta_systole": 140.0,
  "personnels_medicaux_hta": 1,
  "personnels_medicaux_diabete_1": 0,
  "personnels_medicaux_diabete_2": 0,
  "personnels_medicaux_irc": 1,
  "personnels_medicaux_maladies_cardiovasculaire": 1,
  "motif_admission_oedeme": 1,
  "symptomes_asthenie": 1,
  "symptomes_nausees": 0,
  "symptomes_vomissements": 1,
  "symptomes_perte_poids": 0,
  "etat_general_omi": 1,
  "imc": 2,
  "na": 138.0,
  "ca": 91.94,
  "grosseur_rein_gauche": 1,
  "grosseur_rein_droit": 1,
  "echogenicite": 1,
  "dfge": 4.71
}
Réponse
Code : 200 OK (succès)

Body (exemple) :

json
Copy
{
  "prediction": 3,
  "confidence": 0.821
}
Champs Obligatoires
Tous les champs doivent être fournis. Types attendus :

float : creatinine, ta_systole, na, ca, dfge

int (0 ou 1) : Variables binaires (ex: HTA, diabète)

int (0 à 4) : imc (0=Underweight, 1=Normal, etc.)

Codes d'Erreur
422 Unprocessable Entity : Si un champ est manquant ou mal formaté.

500 Internal Server Error : Erreur lors de la prédiction (détails dans le body).

Exemple d'Utilisation
cURL
bash
Copy
curl -X POST "http://127.0.0.1:8000/predict" \
-H "Content-Type: application/json" \
-d '{
  "creatinine": 99.89,
  "ta_systole": 140.0,
  "personnels_medicaux_hta": 1,
  [...autres champs...]
}'
Python (requests)
python
Copy
import requests

data = {
    "creatinine": 99.89,
    "ta_systole": 140.0,
    [...]  # Remplir tous les champs
}

response = requests.post("http://127.0.0.1:8000/predict", json=data)
print(response.json())
Détails des Variables
Variable	Description	Valeurs/Unités
creatinine	Taux de créatinine sérique	mg/L
dfge	Débit de Filtration Glomérulaire estimé	mL/min/1.73m²
ta_systole	Tension artérielle systolique	mmHg
personnels_medicaux_hta	Antécédent d'hypertension	0=Non, 1=Oui
imc	Indice de Masse Corporelle	0=Underweight, 1=Normal, 2=Overweight, 3=Obese, 4=Extremely Obese
grosseur_rein_gauche/droit	Taille du rein	0=Réduit, 1=Normal, 2=Augmenté
Notes
Le modèle retourne des stades 1 à 5 (CKD 1 à CKD 5).

La confiance est une valeur entre 0 et 1 (ex: 0.821 = 82.1%).

Pour exécuter localement : uvicorn main:app --reload (après correction de _name_ en __name__).

Cette documentation peut être enrichie avec :

Un exemple Swagger/OpenAPI intégré (via FastAPI's /docs).

Des détails supplémentaires sur les seuils cliniques des variables.
