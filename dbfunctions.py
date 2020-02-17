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

	try:
		job_descriptions_query = """
			SELECT description FROM job_descriptions WHERE job_id = %(job_id)s
		"""
		cur.execute(job_descriptions_query, {'job_id': job_id})
		results = cur.fetchone()

		output.update({
			'description': results[0]
		})
	except Exception:
		pass

	try:
		job_keyphrases_query = """
			SELECT keyphrase FROM job_keyphrases WHERE job_id = %(job_id)s
		"""
		cur.execute(job_keyphrases_query, {'job_id': job_id})
		results = [result[0] for result in cur.fetchall()]

		output.update({
			'keyphrases': results,
		})
	except Exception:
		pass

	try:
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
	except Exception:
		pass

	try:
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
	except Exception:
		pass

	try:
		job_links_query = """
			SELECT external_url
			FROM job_links
			WHERE job_id = %(job_id)s
			LIMIT 1;
		"""
		cur.execute(
			job_links_query,
			{'job_id': job_id}
		)
		results = cur.fetchone()

		output.update({
			'link': results[0],
		})
	except Exception:
		pass

	cur.close()

	return output


def get_jobs(db, count=100, city=None, state_province=None, country='US', title=None):
	state_province = handle_state_province(state_province)

	cur = db.cursor()
	location_subquery = ''
	if None not in [city, state_province, country]:
		location_subquery = '''
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
		'''

	job_results_query = f'''
		SELECT job_listings.id, job_listings.title, job_listings.post_date_utc
		FROM job_listings
		{location_subquery}
		ORDER BY random()
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


def handle_state_province(state_province):
	if state_province is not None and len(state_province) < 4:
		try:
			state_province = abbr_to_state(state_province)
		except Exception as e:
			pass
	return state_province


def abbr_to_state(abbr):
	return {
		'DC': 'District of Columbia',
		'AL': 'Alabama',
		'MT': 'Montana',
		'AK': 'Alaska',
		'NE': 'Nebraska',
		'AZ': 'Arizona',
		'NV': 'Nevada',
		'AR': 'Arkansas',
		'NH': 'New Hampshire',
		'CA': 'California',
		'NJ': 'New Jersey',
		'CO': 'Colorado',
		'NM': 'New Mexico',
		'CT': 'Connecticut',
		'NY': 'New York',
		'DE': 'Delaware',
		'NC': 'North Carolina',
		'FL': 'Florida',
		'ND': 'North Dakota',
		'GA': 'Georgia',
		'OH': 'Ohio',
		'HI': 'Hawaii',
		'OK': 'Oklahoma',
		'ID': 'Idaho',
		'OR': 'Oregon',
		'IL': 'Illinois',
		'PA': 'Pennsylvania',
		'IN': 'Indiana',
		'RI': 'Rhode Island',
		'IA': 'Iowa',
		'SC': 'South Carolina',
		'KS': 'Kansas',
		'SD': 'South Dakota',
		'KY': 'Kentucky',
		'TN': 'Tennessee',
		'LA': 'Louisiana',
		'TX': 'Texas',
		'ME': 'Maine',
		'UT': 'Utah',
		'MD': 'Maryland',
		'VT': 'Vermont',
		'MA': 'Massachusetts',
		'VA': 'Virginia',
		'MI': 'Michigan',
		'WA': 'Washington',
		'MN': 'Minnesota',
		'WV': 'West Virginia',
		'MS': 'Mississippi',
		'WI': 'Wisconsin',
		'MO': 'Missouri',
		'WY': 'Wyoming',
	}[abbr]
