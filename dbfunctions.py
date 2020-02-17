import psycopg2


def get_details(job_id, db):
	job_listings_query = """
		SELECT * FROM job_listings WHERE id = %(job_id)s
	"""
	cur = db.cursor()
	cur.execute(job_listings_query, {'job_id': job_id})
	results = cur.fetchone()

	output = {
		'job_id': results[0],
		'title': results[1],
		'post_timestamp': results[2],
		'pay_min': results[3],
		'pay_max': results[4],
		'pay_exact': results[5],
		'seniority': results[6]
	}

	job_descriptions_query = """
		SELECT * FROM job_descriptions WHERE job_id = %(job_id)s
	"""
	cur.execute(job_descriptions_query, {'job_id': job_id})
	results = cur.fetchone()

	output.update({
		'description': results[2]
	})

	job_keyphrases_query = """
		SELECT * FROM job_keyphrase WHERE job_id = %(job_id)s
	"""
	cur.execute(job_keyphrases_query, {'job_id': job_id})
	results = [result[2] for result in cur.fetchall()]

	output.update({
		'keyphrases': results,
	})

	job_companies_query = """
		SELECT *
		FROM job_companies
		INNER JOIN companies
		ON job_companies.company_id = companies.id
		WHERE job_id = %(job_id)s
		LIMIT 1
	"""
	cur.execute(
		job_companies_query,
		{'job_id': job_id}
	)
	results = cur.fetchone()

	output.update({
		'company_name':results[4],
		'company_description': results[5],
		'company_size': results[6],
		'company_revenue':results[7]
	})

	job_locations_query = """
		SELECT *
		FROM job_locations
		INNER JOIN locations
		ON job_locations.location_id = locations.id
		WHERE job_id = %(job_id)s
		LIMIT 1;
	"""
	cur.execute(
		job_locations_query,
		{'job_id': job_id}
	)
	results = cur.fetchone()

	output.update({
		'location_city': results[4],
		'location_state_province': results[5],
		'location_country': results[6]
	})

	cur.close()

	return output


def get_jobs(db, count=100, location=None):
	cur = db.cursor()
	job_results_query = """SELECT id, title, post_date_utc FROM job_listings ORDER BY random() LIMIT %(count)s"""
	cur.execute(
		job_results_query,
		{
			'count': count,
			'location': location
		}
	)
	results = cur.fetchall()
	cur.close()

	resultList = []
	for result in results:
		resultsjson = {
			'job_id': result[0],
			'title': result[1],
			'post_timestamp': result[2],
			'relevance': None,
			'resume_score': None,
		}
		resultList.append(resultsjson)

	return resultList
