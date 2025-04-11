from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import uvicorn

# Charger le modèle
model = joblib.load('AI4CKD_best_model.pkl')  # Remplacer par le chemin vers votre modèle


# Définir le modèle de données d'entrée
class InputFeatures(BaseModel):
    creatinine: float
    ta_systole: float
    personnels_medicaux_hta: int
    personnels_medicaux_diabete_1: int
    personnels_medicaux_diabete_2: int
    personnels_medicaux_irc: int
    personnels_medicaux_maladies_cardiovasculaire: int
    motif_admission_oedeme: int
    symptomes_asthenie: int
    symptomes_nausees: int
    symptomes_vomissements: int
    symptomes_perte_poids: int
    
    etat_general_omi: int
    imc: int
    na: float
    ca: float
    grosseur_rein_gauche: int
    grosseur_rein_droit: int
    echogenicite: int
    dfge: float


app = FastAPI()


@app.post("/predict")
def predict(features: InputFeatures):
    # Créer un DataFrame à partir des caractéristiques d'entrée
    try:
        input_data = pd.DataFrame([features.dict()])

        # Obtenir la prédiction
        prediction = model.predict(input_data)[0]
        proba = model.predict_proba(input_data).max()

        # Convertir prediction et proba en types Python standard
        prediction = int(prediction) + 1  # Revenir aux valeurs de stade d'origine
        proba = float(proba)

        # Retourner la prédiction et la probabilité
        return {
            "prediction": prediction,
            "confidence": round(proba, 3)
        }
    except Exception as e:
        return {"error": str(e)}
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)