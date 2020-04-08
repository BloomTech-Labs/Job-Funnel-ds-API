# API Reference

## 1. Table of Contents
<!-- TOC -->

- [1. Table of Contents](#1-table-of-contents)
- [2. Introduction](#2-introduction)
- [3. Resources](#3-resources)
	- [3.1. Searches](#31-searches)
		- [3.1.1. The search object](#311-the-search-object)
			- [3.1.1.1. Attributes](#3111-attributes)
			- [3.1.1.2. Example](#3112-example)
		- [3.1.2. The result object](#312-the-result-object)
			- [3.1.2.1. Attributes](#3121-attributes)
			- [3.1.2.2. Example](#3122-example)
		- [3.1.3. The /search endpoint](#313-the-search-endpoint)
			- [3.1.3.1. Arguments](#3131-arguments)
			- [3.1.3.2. Example request](#3132-example-request)
			- [3.1.3.3. Returns](#3133-returns)
	- [3.2. Job Details](#32-job-details)
		- [3.2.1. The details object](#321-the-details-object)
			- [3.2.1.1. Attributes](#3211-attributes)
			- [3.2.1.2. Example](#3212-example)
		- [3.2.2. The /details endpoint](#322-the-details-endpoint)
			- [3.2.2.1. Arguments](#3221-arguments)
			- [3.2.2.2. Example request](#3222-example-request)
			- [3.2.2.3. Returns](#3223-returns)
	- [3.3. Job Evaluation](#33-job-evaluation)
- [4. Errors](#4-errors)

<!-- /TOC -->

## 2. Introduction

Base URL: http://quickhire-api-dev.j535vysrhe.us-east-1.elasticbeanstalk.com/

The API accepts url-encoded GET requests and returns `app/json` responses.


## 3. Resources


### 3.1. Searches

Searches provide a way for users to search the database for jobs.

#### 3.1.1. The search object

The search object is returned by [the /search endpoint](#313-the-search-endpoint).

##### 3.1.1.1. Attributes

`responses` *List*

A list of [result objects](#312-the-result-object). If no results were found, this list may be empty.

NOTE: Per web team request, this currently instead returns a list of [details objects](#321-the-details-object).

`count` *Int*

The count of results returned.

##### 3.1.1.2. Example
```json
{
	'count': 2,
	'responses': [
		{
			'title': 'Web Developer, Frontend',
			'job_id': 14631,
			'post_timestamp': 1579804925,
			'relevance': null,
			'resume_score': null
		},
		{
			'title': 'Fullstack Engineer',
			'job_id': 14309,
			'post_timestamp': 1579800341,
			'relevance': null,
			'resume_score': null
		}
	]
}
```

#### 3.1.2. The result object

Several result objects are included in each [search object](#311-the-search-object), which is returned by [the /search endpoint](#313-the-search-endpoint).

##### 3.1.2.1. Attributes

`title` *String*

The title of the job.

`job_id` *Int*

The id of the job in the database.

`post_timestamp` *Int*

The time and date when the job was posted, in epoch format.

`relevance` *Float* or *null*

The relevance score of the job. Not yet implemented.

`resume_score` *Float* or *null*

If a resume is provided, how well it fits the job. Not yet implemented.

##### 3.1.2.2. Example
```json
{
	'title': 'Technical Writer',
	'job_id': 14111,
	'post_timestamp': 1579721662,
	'relevance': null,
	'resume_score': null
}
```

#### 3.1.3. The /search endpoint

`/search` accepts GET or POST requests.

##### 3.1.3.1. Arguments

`title` *String*, Optional

The job title to search for. If this argument is not present, `keyphrases` is required.

`keyphrases` *List* of *String*, Optional

A list of keyphrases (e.g. skills) to search for. If this argument is not present, `title` is required.

`resume_id` *null*, Optional

ID of a resume to search by. Not yet implemented.

`count` *Int*, Optional

Maximum number of jobs to return. In the future, this will be ordered by relevance.

`threshold` *Float*, Optional

Minimum relevance of jobs to return. Not yet implemented.

`city` *String*, Optional

City in which to search.

`state_province` *String*, Optional

State or province in which to search.

`country` *String*, Optional

Country in which to search.

`before` *Int*, Optional

Timestamp before which the job was posted.

`after` *Int*, Optional

Timestamp after which the job was posted.

`seniority` *String*, Optional

Seniority level of jobs to search for.

`salary_min` *Int*, Optional

Minimum salary of jobs to search for.

`salary_max` *Int*, Optional

Maximum salary of jobs to search for.

##### 3.1.3.2. Example request
```json
{
	'title': 'Developer',
	'keyphrases': [
		'React',
		'Node'
	]
	'count': 10,
	'threshold': 0.4,
	'state_province': 'Nevada',
	'country': 'United States'
}
```

##### 3.1.3.3. Returns

Returns a [search object](#311-the-search-object) if the search succeeds, or an [error](#4-errors) otherwise. Errors will usually be due to a missing required argument or malformed request.


### 3.2. Job Details

Job Details provide additional details about a job listing.

#### 3.2.1. The details object

The details object is returned by [the /details endpoint](#322-the-details-endpoint).

##### 3.2.1.1. Attributes

`title` *String*

The title of the job.

`job_id` *Int*

The id of the job in the database.

`post_timestamp` *Int*

The date the job was added to the database, in epoch time.

`description` *String*

The description of the job.

`location_city` *String*

The city of the job.

`location_state_province` *String*

The state or province of the job.

`location_country` *String*

The country of the job.

`keyphrases` *List* of *String*

Keyphrases associated with the job.

`company_name` *String* or *null*

The company offering the job.

`company_description` *String* or *null*

The description of the company offering the job.

`company_revenue` *Int* or *null*

The revenue of the company offering the job, if available.

`company_size` *Int* or *null*

The employee count of the company offering the job, if available.

`pay_min` *Int* or *null*

The minimum salary of the job, if salary is a range.

`pay_max` *Int* or *null*

The maximum salary of the job, if salary is a range.

`pay_exact` *Int* or *null*

The salary of the job, if available.

`seniority` *String* or *null*

The seniority level of the job.

A link to the app page of the job.

`lambda_hireability` *Float* or *null*

How relevant a job is to Lambda grads. A higher score means the job is more likely to hire a Lambda grad. Not yet implemented.

##### 3.2.1.2. Example

```json
{
	'title': 'Data Engineer',
	'job_id': 13299,
	'post_timestamp': 1579721662,
	'description': 'This is a long job description about the Data Engineer position. Requires 32 years of experience with Tensorflow, and four PhDs.',
	'location_city': 'Toronto',
	'location_state_province': 'Ontario',
	'location_country': 'Canada',
	'keyphrases': ['Data Pipeline', 'Share-based compensation', 'Tensorflow', 'Python', 'R', 'COBOL', 'Internship']
	'company_name': 'George's Data Warehouse',
	'company_description': 'How hard can it be to convert a warehouse into the data kind?',
	'company_revenue': 15000,
	'company_size': null,
	'pay_min': null,
	'pay_max': null,
	'pay_exact': 30000,
	'seniority': 'Entry-level',
	'lambda_hireability': null
}
```

#### 3.2.2. The /details endpoint

`/details` accepts GET or POST requests.

##### 3.2.2.1. Arguments

`job_id` *Int*, Required

The job ID to get details for.

##### 3.2.2.2. Example request
```json
{
	'job_id': 15979
}
```

##### 3.2.2.3. Returns

Returns a [details object](#321-the-details-object) if the job is found, or an [error](#4-errors) otherwise. Errors will usually be due to an invalid job ID.


### 3.3. Job Evaluation

Job evaluation will get more detailed information regarding how well a resume fits a job. Not yet implemented.


## 4. Errors

TODO
