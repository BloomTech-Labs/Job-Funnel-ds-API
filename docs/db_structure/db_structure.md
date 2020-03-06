## Database Tables ##

Provides a summary of tables in the database, and their columns.

Full schema available at [awsrds.schema](./awsrds.schema)

### job_listings ###
```
id
title
post_date_utc
pay_min
pay_max
pay_exact
seniority
```

### companies ###
```
id
name
description
size
revenue
logo_url
```

### locations ###
```
id
city
state_province
country
```

### job_descriptions ###
```
id
job_id
description
```

### job_keyphrases ###
```
id
job_id
keyphrase
```

### job_companies ###
```
id
job_id
company_id
```

### job_locations ###
```
id
job_id
location_id
```

### job_links ###
```
id
job_id
external_url
```

### lda17_topics ###
```
id
job_id
lda0
lda1
...
lda16
```

### skills ###
```
id
name
```

### user_jobs ###
```
id
user_id
job_id
status
```

### user_skills ###
```
id
user_id
skill_id
```

### users ###
```
id
first_name
last_name
email
password
user_type
company_id
location_id
education
about
profile_img
portfolio_url
github_url
linkedin_url
resume
```
