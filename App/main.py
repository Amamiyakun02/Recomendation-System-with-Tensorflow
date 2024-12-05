import numpy as np
import tensorflow as tf
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from App.Models.sector import Sector

from App.db import Session

def getSector(session: Session, result: int) -> Sector:
    sector = session.query(Sector).filter(Sector.index == result).first()
    return sector

# import ML Model
model_path = "App/ml_model/model.h5"
model = tf.keras.models.load_model(model_path)
app = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_session = Session()

class PredictRequest(BaseModel):
    input_data: List[List[int]]
@app.post('/predict')
async def predict(request: PredictRequest):
    input_data = np.array(request.input_data)
    prediction = model.predict([input_data])
    result = np.argmax(prediction.tolist()[0])
    sectors = getSector(db_session, result+1)
    data = {
        'prediction': int(result),
        'data' : {
            'id' : int(sectors.id),
            'sector': sectors.name,
        }
    }
    return JSONResponse(content=data, status_code=200)