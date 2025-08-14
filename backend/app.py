from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import json
from typing import Literal

app = FastAPI(title="Cervical Cancer Prediction API",
              description="API for predicting cervical cancer risk based on patient attributes")

# Load model and feature names
model = joblib.load('cervical_cancer_model.pkl')
with open("feature_columns.json", "r", encoding='utf-8') as f:
    feature_names = json.load(f)




class PatientInput(BaseModel):
    Age: float
    Number_of_sexual_partners: float
    First_sexual_intercourse: float
    Num_of_pregnancies: float
    Smokes: float
    Smokes_years: float
    Smokes_packs_year: float
    Hormonal_Contraceptives: float
    Hormonal_Contraceptives_years: float
    IUD: float
    IUD_years: float
    STDs: float
    STDs_number: float
    STDs_vaginal_condylomatosis: float
    STDs_vulvo_perineal_condylomatosis: float
    STDs_syphilis: float
    STDs_pelvic_inflammatory_disease: float
    STDs_genital_herpes: float
    STDs_molluscum_contagiosum: float
    STDs_HIV: float
    STDs_Hepatitis_B: float
    STDs_HPV: float
    STDs_Number_of_diagnosis: float
    Dx_Cancer: float
    Dx_CIN: float
    Dx_HPV: float
    Dx: float
    Hinselmann: float
    Schiller: float
    Citology: float

class PredictionOutput(BaseModel):
    prediction: Literal[0, 1]
    risk_level: Literal["Low", "High"]
    probability_percent: float
    interpretation: str

@app.post("/predict", response_model=PredictionOutput)
async def predict(patient: PatientInput):
    # Convert input to numpy array
    features = np.array([[
        patient.Age,
        patient.Number_of_sexual_partners,
        patient.First_sexual_intercourse,
        patient.Num_of_pregnancies,
        patient.Smokes,
        patient.Smokes_years,
        patient.Smokes_packs_year,
        patient.Hormonal_Contraceptives,
        patient.Hormonal_Contraceptives_years,
        patient.IUD,
        patient.IUD_years,
        patient.STDs,
        patient.STDs_number,
        patient.STDs_vaginal_condylomatosis,
        patient.STDs_vulvo_perineal_condylomatosis,
        patient.STDs_syphilis,
        patient.STDs_pelvic_inflammatory_disease,
        patient.STDs_genital_herpes,
        patient.STDs_molluscum_contagiosum,
        patient.STDs_HIV,
        patient.STDs_Hepatitis_B,
        patient.STDs_HPV,
        patient.STDs_Number_of_diagnosis,
        patient.Dx_Cancer,
        patient.Dx_CIN,
        patient.Dx_HPV,
        patient.Dx,
        patient.Hinselmann,
        patient.Schiller,
        patient.Citology
    ]])
    
    try:
        # Get prediction and probability
        prediction = int(model.predict(features)[0])
        probability = model.predict_proba(features)[0][1]
        probability_percent = round(probability * 100, 2)
        
        # Determine risk level and interpretation
        risk_level = "High" if prediction == 1 else "Low"
        
        if probability_percent < 20:
            interpretation = "Very low risk"
        elif probability_percent < 40:
            interpretation = "Low risk"
        elif probability_percent < 60:
            interpretation = "Moderate risk"
        elif probability_percent < 80:
            interpretation = "High risk"
        else:
            interpretation = "Very high risk"
        
        return {
            "prediction": prediction,
            "risk_level": risk_level,
            "probability_percent": probability_percent,
            "interpretation": interpretation
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")