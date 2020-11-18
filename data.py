import pandas as pd
import numpy as np
from sodapy import Socrata

COLS2 = [
    "fecha reporte web",
    "ID de caso",
    "Fecha de notificación",
    "Código DIVIPOLA departamento",
    "Nombre departamento",
    "Código DIVIPOLA municipio",
    "Nombre municipio",
    "Edad",
    "Unidad de medida de edad",
    "Sexo",
    "Tipo de contagio",
    "Ubicación del caso",
    "Estado",
    "Código del país viajo",
    "Nombre del país viajo",
    "Recuperado",
    "Fecha de inicio de síntomas",
    "Fecha de diagnóstico",
    "Fecha de recuperación",
    "Tipo de recuperación",
    "Pertenencia étnica",
    "Nombre del grupo étnico",
    "Fecha de muerte",
]

COLS = [
    "fweb",
    "id",
    "fnot",
    "cdep",
    "ndep",
    "cmun",
    "nmun",
    "edad",
    "uedad",
    "sexo",
    "tipo",
    "ubic",
    "estado",
    "cpais",
    "npais",
    "recu",
    "fsin",
    "fdia",
    "frec",
    "trec",
    "etnia",
    "netnia",
    "fmuer",
]


def get_data(url, id, lmt):
    client = Socrata(url, None)
    results = client.get(id, limit=lmt)
    return pd.DataFrame.from_records(results)


def normalize(dataframe):
    dates = ["fweb", "fnot", "fsin", "fdia", "frec", "fmuer"]
    strings = [
        "ndep",
        "nmun",
        "uedad",
        "sexo",
        "tipo",
        "ubic",
        "estado",
        "npais",
        "recu",
        "trec",
        "etnia",
        "netnia",
    ]

    df = dataframe.rename(
        columns={
            "fecha_reporte_web": "fweb",
            "id_de_caso": "id",
            "fecha_de_notificaci_n": "fnot",
            "departamento": "cdep",
            "departamento_nom": "ndep",
            "ciudad_municipio": "cmun",
            "ciudad_municipio_nom": "nmun",
            "edad": "edad",
            "unidad_medida": "uedad",
            "sexo": "sexo",
            "fuente_tipo_contagio": "tipo",
            "ubicacion": "ubic",
            "estado": "estado",
            "recuperado": "recu",
            "fecha_inicio_sintomas": "fsin",
            "fecha_diagnostico": "fdia",
            "fecha_recuperado": "frec",
            "tipo_recuperacion": "trec",
            "per_etn_": "etnia",
            "fecha_muerte": "fmuer",
            "nom_grupo_": "netnia",
            "pais_viajo_1_cod": "cpais",
            "pais_viajo_1_nom": "npais",
        }
    )

    uedad = {"1": "Años", "2": "Meses", "3": "Días"}
    etnia = {
        "1": "Indígena",
        "2": "ROM",
        "3": "Raizal",
        "4": "Palenquero",
        "5": "Negro",
        "6": "Otro",
    }

    df["uedad"] = df["uedad"].apply(lambda x: uedad[x] if not pd.isna(x) else np.nan)

    df["etnia"] = df["etnia"].apply(lambda x: etnia[x] if not pd.isna(x) else np.nan)

    for date in dates:
        df[date] = pd.to_datetime(df[date], errors="ignore", dayfirst=True)

    for string in strings:
        df[string] = df[string].str.title()

    df = df.astype(
        {
            "id": "int32",
            "cdep": "int32",
            "cmun": "int32",
            "edad": "int32",
            "cpais": "int32",
        },
        errors="ignore",
    )

    return df


def by_date(col, dates):
    query = " or ".join(['{} == "{}"'.format(col, f) for f in dates])
    return query


def by_string(col, values):
    query = " or ".join(['{} == "{}"'.format(col, value) for value in values])
    return query


def by_numbers(dataframe, col, values, op):
    query = " or ".join(
        ["{} {} {}".format(col, pair[0], pair[1]) for pair in zip(op, values)]
    )
    return query
