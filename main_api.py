import csv
import codecs
import pickle
import uvicorn
import pandas as pd
from joblib import load
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, File, UploadFile, BackgroundTasks

app = FastAPI()

COLUMNS = ["numero_aviso",	"marca", "codigo_irs", "nombre", "marca.1", "anio",
           "linea", "grupo", "subgrupo", "tipo_carroceria"]

with open("model/all_columns.pickle", "rb") as f:
    all_columns = pickle.load(f)


def anio_group(anio):
    """
    this function calculate year range
    :param anio: int, year made
    :return: str, year range
    """
    if anio <= 2024 and anio >= 2021:
        anio_range = "2024 - 2021"
    elif anio <= 2020 and anio >= 2017:
        anio_range = "2020 - 2017"
    elif anio <= 2016 and anio >= 2013:
        anio_range = "2016 - 2013"
    elif anio <= 2012 and anio >= 2009:
        anio_range = "2012 - 2009"
    elif anio <= 2008 and anio >= 2005:
        anio_range = "2008 - 2005"
    else:
        anio_range = "2004 - atrás"

    return anio_range


@app.post("/upload_file/")
def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """

    :param background_tasks: upload .csv file
    :param file: file to read with columns: "numero_aviso",	"marca", "codigo_irs", "nombre", "marca.1", "anio",
    "linea", "grupo", "subgrupo", "tipo_carroceria"
    :return: json with prediction
    """
    csv_reader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
    df_user = pd.DataFrame(list(csv_reader))
    background_tasks.add_task(file.file.close)

    df_user.columns = COLUMNS

    df = df_user.drop(columns=["numero_aviso",
                               "marca",
                               "linea",
                               "nombre"])

    df["anio"] = df["anio"].astype(int)

    anio_range_list = list(map(anio_group, list(df["anio"])))
    df["anio_range"] = anio_range_list
    df = df.drop(columns=["anio"])

    df["grupo"] = df["grupo"].astype(str)
    df["subgrupo"] = df["subgrupo"].astype(str)

    df_model = pd.get_dummies(df)

    for i in range(len(all_columns)):
        if all_columns[i] not in df_model.columns:
            df_model[all_columns[i]] = 0

    X = df_model.values

    lr_model = load('model/lr_class.joblib')

    action = []
    for i in range(len(X)):
        temp = lr_model.predict(X[i].reshape(1, -1))[0]
        if temp:
            temp2 = "cambiar"
        else:
            temp2 = "reparar"
        action.append(temp2)

    df_user["action"] = action

    json_compatible_data = jsonable_encoder(df_user)

    return JSONResponse(content=json_compatible_data)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8090)
