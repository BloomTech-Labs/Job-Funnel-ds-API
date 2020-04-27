import psycopg2
import re


def get_details(job_id, db):
	job_listings_query = """
		SELECT id, title, EXTRACT(epoch FROM post_date_utc), pay_min, pay_max, pay_exact, seniority FROM job_listings WHERE id = %(job_id)s
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
		output.update({
			'description': None
		})

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
		output.update({
			'keyphrases': []
		})

	try:
		job_companies_query = """
			SELECT name, description, size, revenue, logo_url
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
			'company_revenue': results[3],
			'company_logo_url': results[4],
		})
	except Exception:
		output.update({
			'company_name': None,
			'company_description': None,
			'company_size': None,
			'company_revenue': None,
			'company_logo_url': None,
		})

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
		output.update({
			'location_city': None,
			'location_state_province': None,
			'location_country': None
		})

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
		output.update({
			'link': None
		})

	cur.close()

	return output


def get_jobs(db, count=100, city=None, state_province=None, country='US', title=None, before=None, after=None, salary_min=None, salary_max=None, seniority=None):
	state_province = handle_state_province(state_province)
	cur = db.cursor()
	exact_location_subquery = '''
		WHERE TRUE
	'''
	if city is not None:
		exact_location_subquery += '''
			AND city = %(city)s
		'''
	if state_province is not None:
		exact_location_subquery += '''
			AND state_province = %(state_province)s
		'''
	if country is not None:
		exact_location_subquery += '''
			AND country ILIKE %(country)s
		'''
	location_subquery = f'''
		INNER JOIN (
			SELECT *
			FROM job_locations
			INNER JOIN (
				SELECT *
				FROM locations
				{exact_location_subquery}
			) AS loc
			ON job_locations.location_id = loc.id
		) AS jobs_locs
		ON job_listings.id = jobs_locs.job_id
	'''
	# filters only for key words that are probably in tech jobs
	# can probably be removed after cron job to filter database is done
	# ILIKE is Postgres specific and makes things case insensitive
	job_details_subquery = '''
		WHERE 
		    title ILIKE '%%developer'
	 		OR title ILIKE '%%designer'
	 		OR title ILIKE '%%programmer'
	 		OR title ILIKE '%%data'
	 		OR title ILIKE '%%engineer'
			OR title ILIKE '%%analyst'
			OR title ILIKE '%%QA'
			OR title ILIKE '%%UX'
			OR title ILIKE '%%UI'
			OR title ILIKE '%%dev'
			OR title ILIKE '%%HCI'
			OR title ILIKE '%%software'
			OR title ILIKE '%%database'
			OR title ILIKE '%%web'
			OR title ILIKE '%%iOS'
			OR title ILIKE '%%Android'
			OR title ILIKE '%%mobile'
	'''
	if before is not None:
		job_details_subquery += '''
			AND post_date_utc < TO_TIMESTAMP(%(before)s)
		'''
	if after is not None:
		job_details_subquery += '''
			AND post_date_utc > TO_TIMESTAMP(%(after)s)
		'''
	if seniority is not None:
		job_details_subquery += '''
			AND seniority ILIKE %(seniority)s
		'''
	if salary_min is not None:
		job_details_subquery += '''
			AND (
				pay_min > %(salary_min)s
				OR pay_exact > %(salary_min)s
			)
		'''
	if salary_max is not None:
		job_details_subquery += '''
			AND (
				pay_max > %(salary_max)s
				OR pay_exact > %(salary_max)s
			)
		'''
		
	title_params = {}
	if title is not None:
		title_parts = title.split()
		for i, title_part in enumerate(title_parts):
			key = f'title_part_{i}'
			title_params[key] = f'%{title_part}%'
			job_details_subquery += f'''
				AND title ILIKE %({key})s
			'''
	# final combined query, filtered by most recent post date
	job_results_query = f"""
		SELECT job_listings.id, job_listings.title, EXTRACT(epoch FROM job_listings.post_date_utc)
		FROM job_listings
		{location_subquery}
		{job_details_subquery}
		ORDER BY job_listings.post_date_utc DESC
		LIMIT %(count)s;
	"""

	if city is not None:
		city = titlecase(city)
	if state_province is not None:
		state_province = titlecase(state_province)
	params = {
		'count': count,
		'city': city,
		'state_province': state_province,
		'country': country,
		'before': before,
		'after': after,
		'seniority': seniority,
		'salary_min': salary_min,
		'salary_max': salary_max,
		'title': title,
	}
	params.update(title_params)

	try:
		cur.execute(
			job_results_query,
			params
		)
		results = cur.fetchall()

		resultList = []
		for result in results:
			try:
				resultsjson = {
					'job_id': result[0],
					'title': result[1],
					'post_timestamp': result[2],
					'relevance': None,
					'resume_score': None,
				}
				resultsjson.update(get_details(result[0], db))
				resultList.append(resultsjson)
			except Exception:
				pass

	except Exception as e:
		resultList = []

	finally:
		cur.close()

	return resultList


def handle_state_province(state_province):
	if state_province is not None and len(state_province) < 4:
		try:
			state_province = abbr_to_state(state_province)
		except Exception as e:
			pass
	return state_province


def titlecase(s: str) -> str:
	"""
	Titlecases a string in a stricter manner.
		Does not fail on symbols and apostrophes.

	Args:
		s (str): string to titlecase

	Returns:
		str: titlecased string
	"""

	return (
		re.sub(
			r"^[A-Za-z]+",
			lambda mo: mo.group(0)[0].upper() + mo.group(0)[1:].lower(),
			re.sub(
				r"(?<=[\n 	])[A-Za-z]+",
				lambda mo: mo.group(0)[0].upper() + mo.group(0)[1:].lower(),
				s
			)
		)
	)


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
