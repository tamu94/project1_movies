import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
import warnings
import config
import pymysql
import os

USER = "root"
PASSWORD = config.password
HOST = "127.0.0.1"
PORT = "3306"
DATABASE = "movies_db"
TABLENAME = "movies"

filepath = os.path.join("Results", "tmbd_data_final.csv")
df = pd.read_csv(filepath)

engine = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}")

try:
    engine.execute(f"CREATE DATABASE {DATABASE}")
except ProgrammingError:
    warnings.warn(f"Could not create database {DATABASE}. Database {DATABASE} may already exist.")
    pass

engine.execute(f"USE {DATABASE}")
engine.execute(f"DROP TABLE IF EXISTS {TABLENAME}")
df.to_sql(name=TABLENAME, con=engine)