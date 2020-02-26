from flask import Flask, jsonify, request
import psycopg2
from dbfunctions import get_jobs
from decouple import config
import pandas as pd


def get_details(conn):

    cur = conn.cursor()

    job_descriptions_query = """
        SELECT * FROM job_descriptions WHERE id>1000
    """
    cur.execute(job_descriptions_query)
    results = cur.fetchall()

    return results

with psycopg2.connect(dbname=config("DB_DB"),
user=config("DB_USER"), password=config("DB_PASSWORD"),
host=config("DB_HOST"), port=config("DB_PORT")) as psql_conn:

    job_d = get_details(psql_conn)

df = pd.DataFrame(job_d)
df.to_csv('lda_test_1000.csv')
