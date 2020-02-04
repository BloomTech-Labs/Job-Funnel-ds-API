from flask import Flask, jsonify, request
from dbfunctions import get_details
import psycopg2
from dbfunctions import get_jobs
from decouple import config

app = Flask(__name__)

@app.route('/search')
def search():
    """ when someone types /search in the url this function will work to
    present what we want for this page """
    with psycopg2.connect(dbname=config("DB_DB"),
    user=config("DB_USER"), password=config("DB_PASSWORD"),
    host=config("DB_HOST"), port=config("DB_PORT")) as psql_conn:
        output = get_jobs(psql_conn)
    return jsonify(output)



@app.route('/details')
def details():
    """ when someone types /details in the url this function will work to
    present what we want for this page """
    input = request.get_json()
    job_id = input.get('job_id', None)
    if job_id is None:
        raise NotImplementedError('not')
    with psycopg2.connect(dbname=config("DB_DB"),
    user=config("DB_USER"), password=config("DB_PASSWORD"),
    host=config("DB_HOST"), port=config("DB_PORT")) as psql_conn:
        output = get_details(job_id, psql_conn)
    return jsonify(output)

if __name__ == "__main__":
    app.run()
