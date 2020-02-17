import psycopg2


def get_details(job_id, db):
	job_listings_query = """
		SELECT id, title, post_date_utc, pay_min, pay_max, pay_exact, seniority FROM job_listings WHERE id = %(job_id)s
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
		SELECT description FROM job_descriptions WHERE job_id = %(job_id)s
	"""
	cur.execute(job_descriptions_query, {'job_id': job_id})
	results = cur.fetchone()

	output.update({
		'description': results[0]
	})

	job_keyphrases_query = """
		SELECT keyphrase FROM job_keyphrases WHERE job_id = %(job_id)s
	"""
	cur.execute(job_keyphrases_query, {'job_id': job_id})
	results = [result[0] for result in cur.fetchall()]

	output.update({
		'keyphrases': results,
	})

	job_companies_query = """
		SELECT name, description, size, revenue
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
		'company_name': results[0],
		'company_description': results[1],
		'company_size': results[2],
		'company_revenue': results[3]
	})

	job_locations_query = """
		SELECT city, state_province, country
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
		'location_city': results[0],
		'location_state_province': results[1],
		'location_country': results[2]
	})

	cur.close()

	return output


def get_jobs(db, count=100, city=None, state_province=None, country='US', title=None):
	cur = db.cursor()
	job_results_query = """SELECT id, title, post_date_utc FROM job_listings ORDER BY random() LIMIT %(count)s"""
	if None not in [city, state_province, country]:
		job_results_query = '''
			SELECT job_listings.id, job_listings.title, job_listings.post_date_utc
			FROM job_listings
			INNER JOIN (
				SELECT *
				FROM job_locations
				INNER JOIN (
					SELECT *
					FROM locations
					WHERE city=%(city)s
						AND state_province=%(state_province)s
						AND country=%(country)s
				) AS loc
				ON job_locations.location_id = loc.id
			) AS jobs_locs
			ON job_listings.id = jobs_locs.job_id
			LIMIT %(count)s;
		'''
	cur.execute(
		job_results_query,
		{
			'count': count,
			'city': city,
			'state_province': state_province,
			'country': country
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
