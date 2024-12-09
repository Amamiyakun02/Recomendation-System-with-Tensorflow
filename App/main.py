import numpy as np
import tensorflow as tf
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from App.Models.database_models import Sector, Universitas
from App.db import Session

#d utils function
def getMultiSector(probability):
    top_indices = []
    for _ in range(3):
        y = np.argmax(np.array(probability))
        top_indices.append(y)
        probability[0, y] = 0
    return top_indices

def getSectorData(session: Session, sector_name) -> Sector:
    sector = session.query(Sector).filter(Sector.nama_sektor == sector_name).first()
    return sector

# CONSTANT
SECTOR = np.array([
    "IT Sector",
    "Goverment Sector",
    "Health Sector",
    "Education Sector",
    "Sports Sector",
    "Finance Sector",
    "Entertainment Sector"
])
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

    try:
        input_data = np.array(request.input_data)
        prediction = model.predict([input_data])
        sector = SECTOR[np.argmax(prediction)]
        print("Sector : ", sector)
        result = getSectorData(db_session, sector_name=sector)

        universitas = []
        for univ in result.universitas:
            universitas.append({
                "id": univ.id_universitas,
                "name": univ.universitas,
                "jurusan": univ.jurusan,
                "sector": result.nama_sektor,
                "website" : univ.url_website,
                "description": univ.deskripsi,
            })

        response_data = {
        "data":{
            "predict": {
                "sector" :[
                    {
                        "id" : result.id_sektor,
                        "name" : result.nama_sektor,
                        "university" : universitas
                    }
                ]
            },
            "accuracy" : 0.98
        },
        "message" : "Successfuly",
        "error" : False,
    }

        return JSONResponse(content=response_data, status_code=200)

    except Exception as e:
        response_data = {
            "data":{
                "error" : str(e),
            },
            "message" : "Error",
            "error": True,
        }
        return JSONResponse(content=response_data, status_code=500)

@app.post('/multi-predict')
async def multi_predict(request: PredictRequest):

    try:
        input_data = np.array(request.input_data)
        prediction = model.predict([input_data])
        sectors = []
        universitas = []

        for sector in getMultiSector(prediction):
            print(SECTOR[sector])
            result = getSectorData(db_session, sector_name=SECTOR[sector])
            print(bool(result.universitas))
            for univ in result.universitas:
                universitas.append(
                    {
                        "id": univ.id_universitas,
                        "name": univ.universitas,
                        "jurusan": univ.jurusan,
                        "sector": result.nama_sektor,
                        "website": univ.url_website,
                        "description": univ.deskripsi,
                    }
                )
            sectors.append({
                "id": result.id_sektor,
                "name": result.nama_sektor,
                "university" : universitas
            })
            # else:
            #     sectors.append({
            #         "id": result.id_sektor,
            #         "name": result.nama_sektor,
            #         "university": []
            #     })
        response_data = {
            "data":{
                "sector" : sectors,
            }
        }
        return JSONResponse(content=response_data, status_code=200)

    except Exception as e:
        response_data = {
            "data":{
                "error" : str(e),
            },
            "message" : "Error",
            "error": True,
        }
        return JSONResponse(content=response_data, status_code=500)
