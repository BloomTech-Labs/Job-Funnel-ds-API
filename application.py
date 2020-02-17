from flask import Flask, jsonify, request
from dbfunctions import get_details
import psycopg2
from dbfunctions import get_jobs
from decouple import config

application = Flask(__name__)


@application.route('/search')
def search():
	""" when someone types /search in the url this function will work to
	present what we want for this page """

	count = request.args.get('count', 100)
	with psycopg2.connect(
			dbname=config("DB_DB"),
			user=config("DB_USER"),
			password=config("DB_PASSWORD"),
			host=config("DB_HOST"),
			port=config("DB_PORT")
	) as psql_conn:
		output = get_jobs(psql_conn, count=count)
	ret = {
		'count': len(output),
		'responses': output
	}
	return jsonify(ret)


@application.route('/details')
def details():
	""" when someone types /details in the url this function will work to
	present what we want for this page """
	# args = request.get_json()
	args = request.args  # Use query args for simplicity for now
	job_id = args.get('job_id', None)
	if job_id is None:
		output = {
			'error': 'job_id parameter is required'
		}
		return jsonify(output)
	with psycopg2.connect(
			dbname=config("DB_DB"),
			user=config("DB_USER"),
			password=config("DB_PASSWORD"),
			host=config("DB_HOST"),
			port=config("DB_PORT")
	) as psql_conn:
		output = get_details(job_id, psql_conn)
	return jsonify(output)


if __name__ == "__main__":
	application.run()
