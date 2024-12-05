import numpy as np
import tensorflow as tf
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from App.Models.sector import Sector

from App.db import Session

def getSectorData(session: Session, sector_name) -> Sector:
    sector = session.query(Sector).filter(Sector.nama_sektor == sector_name).first()
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
    sector_data = np.array([
        "IT Sector",
        "Goverment Sector",
        "Health Sector",
        "Education Sector",
        "Sports Sector",
        "Finance Sector",
        "Entertainment Sector"
    ])

    input_data = np.array(request.input_data)
    prediction = model.predict([input_data])
    sector = sector_data[np.argmax(prediction)]
    print(sector)
    result = getSectorData(db_session, sector_name=sector)
    data = {
        'prediction': int(np.argmax(prediction)),
        'data' : {
            'id' : int(result.id_sektor),
            'sector': result.nama_sektor,
        }
    }

    return JSONResponse(content=data, status_code=200)