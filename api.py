# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 13:15:31 2024
@author: Windows
"""

from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import pandas as pd
from db_connection import engine
import os

app = FastAPI()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Rutas de los archivos CSV
CSV_FILE_USER = os.path.join(os.path.dirname(__file__), "users - users.csv")
CSV_FILE_PROFILE = os.path.join(os.path.dirname(__file__), "profiles - Hoja 1.csv")
CSV_FILE_RESUME = os.path.join(os.path.dirname(__file__), "resumes - resumes.csv")
CSV_FILE_CHALLENGE = os.path.join(os.path.dirname(__file__), "challenges - challenges.csv")

@app.post("/upload_csv_local/")
async def upload_csv_local():
    try:
        
        for file_path, name in [(CSV_FILE_USER, "usuarios"), (CSV_FILE_PROFILE, "perfiles"), 
                                (CSV_FILE_RESUME, "resumes"), (CSV_FILE_CHALLENGE, "challenges")]:
            if not os.path.isfile(file_path):
                raise HTTPException(status_code=404, detail=f"Archivo CSV de {name} no encontrado.")

        # Leer y procesar cada archivo CSV
        data_users = pd.read_csv(CSV_FILE_USER).where(pd.notna(pd.read_csv(CSV_FILE_USER)), None)
        data_profiles = pd.read_csv(CSV_FILE_PROFILE).where(pd.notna(pd.read_csv(CSV_FILE_PROFILE)), None)
        data_resumes = pd.read_csv(CSV_FILE_RESUME).where(pd.notna(pd.read_csv(CSV_FILE_RESUME)), None)
        data_challenges = pd.read_csv(CSV_FILE_CHALLENGE, encoding="utf-8").where(pd.notna(pd.read_csv(CSV_FILE_CHALLENGE)), None)

        print("Archivos CSV leídos correctamente.")

        # Función para formatear valores
        def format_value(value):
            if value is None:
                return "NULL"
            return f"'{value}'"

        # Preparar inserción para la tabla users
        all_values_users = []
        for _, row in data_users.iterrows():
            values = [format_value(row[col]) for col in data_users.columns]
            all_values_users.append(f"({', '.join(values)})")
        query_users = f"INSERT INTO users ({', '.join(data_users.columns)}) VALUES {', '.join(all_values_users)}"
        print("Consulta para insertar en users:", query_users)

        # Preparar inserción para la tabla profiles
        all_values_profiles = []
        for _, row in data_profiles.iterrows():
            values = [format_value(row[col]) for col in data_profiles.columns]
            all_values_profiles.append(f"({', '.join(values)})")
        query_profiles = f"INSERT INTO profiles ({', '.join(data_profiles.columns)}) VALUES {', '.join(all_values_profiles)}"
        print("Consulta para insertar en profiles:", query_profiles)

        # Preparar inserción para la tabla resumes
        all_values_resumes = []
        for _, row in data_resumes.iterrows():
            values = [format_value(row[col]) for col in data_resumes.columns]
            all_values_resumes.append(f"({', '.join(values)})")
        query_resumes = f"INSERT INTO resumes ({', '.join(data_resumes.columns)}) VALUES {', '.join(all_values_resumes)}"
        print("Consulta para insertar en resumes:", query_resumes)

        # Preparar inserción para la tabla challenges
        all_values_challenges = []
        for _, row in data_challenges.iterrows():
            values = [format_value(row[col]) for col in data_challenges.columns]
            all_values_challenges.append(f"({', '.join(values)})")
        query_challenges = f"INSERT INTO challenges ({', '.join(data_challenges.columns)}) VALUES {', '.join(all_values_challenges)}"
        print("Consulta para insertar en challenges:", query_challenges)

        # Ejecutar todas las inserciones
        with SessionLocal() as connection:
            connection.execute(text(query_users))
            connection.execute(text(query_profiles))
            connection.execute(text(query_resumes))
            connection.commit()

        return {
            "message": f"Datos cargados exitosamente desde CSV: {len(data_users)} en users, {len(data_profiles)} en profiles, {len(data_resumes)} en resumes, {len(data_challenges)} en challenges."
        }

    except Exception as e:
        print(f"Error al procesar el archivo CSV: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 18:09:22 2024

@author: Windows
"""

app = FastAPI()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Ruta del archivo CSV
CSV_FILE_CHALLENGE = os.path.join(os.path.dirname(__file__), "challenges - challenges.csv")

def clean_text(text):
    if pd.notna(text):
        text = text.encode('latin1').decode('utf-8')
    return text

@app.post("/upload_csv_challenges/")
async def upload_csv_challenges():
    try:
        # Verificar si el archivo CSV existe
        if not os.path.isfile(CSV_FILE_CHALLENGE):
            raise HTTPException(status_code=404, detail="Archivo CSV de challenges no encontrado en la ruta especificada.")
        
        # Leer y limpiar el archivo CSV
        data_challenges = pd.read_csv(CSV_FILE_CHALLENGE, encoding="UTF-8")

        print(data_challenges.head())

        def format_value(value):
            if value is None or pd.isna(value):
                return "NULL"
            elif isinstance(value, str):
                # Reemplazar comillas simples y dobles por comillas escapadas para SQL
                return "'" + value.replace("'", "''").replace('"', '""') + "'"
            else:
                return str(value)

        # Preparar la lista de valores para la inserción en batch
        all_values_challenges = []
        for _, row in data_challenges.iterrows():
            values = [
                format_value(row['name']),
                format_value(row['description']),
                format_value(row['status']),
                format_value(row['opencall_objective']),
                format_value(row['created_at'])
            ]
            all_values_challenges.append(f"({', '.join(values)})")
        
        values_str_challenges = ", ".join(all_values_challenges)
        query_challenges = f"INSERT INTO challenges (name, description, status, opencall_objective, created_at) VALUES {values_str_challenges}"

        # Ejecutar la inserción en batch usando `text`
        with SessionLocal() as connection:
            connection.execute(text(query_challenges))
            connection.commit()
            
        return {
            "message": f"Datos de challenges cargados exitosamente desde CSV con {len(data_challenges)} registros."
        }
    
    except Exception as e:
        print(f"Error al procesar el archivo CSV: {e}")
        raise HTTPException(status_code=500, detail=str(e))

