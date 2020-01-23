
# API Reference #

Base URL: TBD

The API accepts `application/json` requests and returns `application/json` responses.


# Resources #

### Searches ###

<a name="search_object"></a>
#### The search object ####

##### Attributes #####

*responses* (`List`)

A list of [result objects](#result_object). If no results were found, this list may be empty.

*count* (`Int`)

The count of results returned.

##### Example #####

```
{
	'count': 2,
	'responses': [
		{
			'title': 'Web Developer, Frontend',
			'job_id': 14631,
			'post_timestamp': 1579804925,
			'relevance': 1.0
		},
		{
			'title': 'Fullstack Engineer',
			'job_id': 14309,
			'post_timestamp': 1579800341,
			'relevance': 1.0
		}
	]
}
```

<a name="result_object"></a>
#### The result object ####

##### Attributes #####

*title* (`String`)

The title of the job.

*job_id* (`Int`)

The id of the job in the database.

*post_timestamp* (`Int`)

The time and date when the job was posted, in epoch format.

*relevance* (`Float`)

The relevance score of the job. Not yet implemented, so will always be 1.0.

##### Example #####

```
{
	'title': 'Technical Writer',
	'job_id': 14111,
	'post_timestamp': 1579721662,
	'relevance': 1.0
}
```

#### The /search Endpoint ####

`/search` accepts GET or POST requests.

##### Arguments #####

*title* (Required)

The job title to search for.

*count*

Maximum number of jobs to return. In the future, this will be ordered by relevance.

*threshold*

Minimum relevance of jobs to return. Not currently implemented.

*city*

City in which to search.

##### Returns #####

Returns a [search object](#search_object) if the search succeeds, or an [error](#errors) otherwise. Errors will usually be due to a missing required argument or malformed request.


<a name="errors"></a>
# Errors #

TODO
