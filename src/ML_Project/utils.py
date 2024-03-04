import os
import sys
from src.ml_project.exception import CustomException
from src.ml_project.logger import logging
import pandas as pd
from dotenv import load_dotenv
import pymysql

load_dotenv()

host=os.getenv("host")
user=os.getenv("user")
pwd=os.getenv("password")
db=os.getenv("db")

def read_sql_data():
    logging.info("Reading SQL database started")

    try:
        mydb=pymysql.connect(
            host=host,
            user=user,
            password=pwd,
            db=db
        )
        logging.info("Connection Established",mydb)

        df=pd.read_sql_query('select * from student',mydb)
        print(df.head())

        return df

    except Exception as e:
        raise CustomException(e,sys=sys)