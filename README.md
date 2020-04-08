### QUICK HIRE

This project is part of the data science group for Labs project Quick Hire. Quick hire is a one stop job app portal for specifically for Lambda School students. 

You can find the live project at [QuickHire.dev](https://quickhire.dev)

## Quickhire DS-API Description

This repository holds code for the Flask app (migration to FastAPI pending) and database functions for the Data Science portion of Quick Hire. It also includes documentation for the code until the migration to FastAPI with its automatically generated documentation is complete. It will also include tests from Starlette (comes with FastAPI) once migration is complete. 

### Methods Used

* Web Scraping
* Machine Learning
* Predictive Modeling
* Deep Learning (to be implemented)
* Code Coverage/Automated Testing (to be implemented)

### Tech Stack

* Python
* Pandas, Jupyter
* FastAPI
* Starlette
* Selenium 
* PostgresSQL 
* AWS Elastic Beanstalk 
* AWS Lambda Functions
* AWS RDS

## QuickHire DS-API More Detailed Description

The database (PostgreSQL) is hosted on AWS RDS (database-1). A summary of the structure can be found at docs/db_structure/db_structure.md, and schema details at docs/db_structure/awsrds.schema.

The web app is hosted on AWS elastic beanstalk. The documentation can be found here: https://github.com/Lambda-School-Labs/Job-Funnel-ds-API/blob/master/docs/api/reference.md until migration to FastAPI is complete.

Test Suite not implemented yet but to be updated here. 

# QuickHire DS-API Documentation

Documentation for this API can be found [here] (https://github.com/Lambda-School-Labs/Job-Funnel-ds-API/tree/master/docs) for: 
* project architecture 
* database structure and schema 
* API/ / reference (until migration to FastAPI is complete)
* project status (pending, may move here) 
* lambda functions deployed to AWS.

See [Backend Documentation](https://github.com/Lambda-School-Labs/Job-Funnel-be) for details on the backend of our project.
See [Frontend Documentation](https://github.com/Lambda-School-Labs/Job-Funnel-fe) for details on the frontend of our project.

## Needs of this Project

# Current and Future Project Status

## 1. Table of Contents
<!-- TOC -->

- [1. Table of Contents](#1-table-of-contents)
- [2. Current](#2-current)
- [3. Future](#3-future)
	- [3.1. Top Priorities](#31-top-priorities)
		- [3.1.1. Implement lda17](#311-implement-lda17)
		- [3.1.2. Investigate best methods of sharing models](#312-investigate-best-methods-of-sharing-models)
		- [3.1.3. Add more scrapers](#313-add-more-scrapers)
	- [3.2. Important Changes](#32-important-changes)
	- [3.3. Minor Fixes](#33-minor-fixes)

<!-- /TOC -->

## 2. Current

See [architecture.md](./architecture.md) for details on the current project state.

There is not currently any code coverage.

## 3. Future

### 3.1. Top Priorities

#### 3.1.1. Implement lda17

No models are currently available on the /search endpoint. This is somewhat unacceptable - using the models to improve search is a crucial part of the project. There is a hacky start to an implementation on the `ds-Data/serve-models` and `ds-API/skills` branches, which serves the models over the `ds-Data` utility API, and provides a _/check\_fresh_ to reload the models if they're more than an hour out of date.

Note that model results should be provided via the `relevance` parameter on jobs returned from the API's `/search` endpoint.

#### 3.1.2. Investigate best methods of sharing models

In the aforementioned hacky methodology, the models are shared between `ds-Data` and `ds-API` over HTTP. This is _not_ a good way of doing this. Amazon EFS is likely the simplest solution, but further investigation may be warranted.

#### 3.1.3. Add more scrapers

### 3.2. Important Changes

- Improve API efficiency
	- Currently, the API gets a list of results, then iterates through each to get the details. This is an artifact of prior API design (where full details were not returned by /search), and is inefficient. Rebuild the queries to fix this.
- Implement Hireability score
	- One of the primary value points of the project, the hireability score is a value that assesses how relevant a job is to Lambda graduates, based on a classification model trained on historical grads (and what jobs they found).
	- If you can't get data from Lambda, might want to scrape LinkedIn for people associated with Lambda School, and what jobs they have.
- Add tests
	- There's not currently any test coverage.

### 3.3. Minor Fixes

- The `quickhire-api-dev` CodePipeline does not automatically pull changes from GitHub. You have to manually release changes.


## Getting Started

NOTE: Master branch of this code is already running live on AWS. If you are the next Lambda School Team to build on, you will inherit the AWS instances and also be given lectures on how to use the various AWS services. 

Nonetheless, if you want to work on this locally:

1. Clone this repo. 

2. Clone the other repo which has the web scraper and models: https://github.com/Lambda-School-Labs/Job-Funnel-ds-Data

3. Create your own database and login credentials setup since the .gitignore has our live database credentials. Install any libraries from requirements of both repos that weren't added. If you are Lambda Labs students, your TL should give you the  AWS DB credentials or .env files. Else you can find them by DM'ing previous team members. 

4. Run the scraper in the other repo to begin populating the data base.

## Featured Notebooks/Tutorials/Additional Resources 

 To be updated

## Contributing

Full Name: Github : Slack Handle 

Please note we have a [code of conduct](./code_of_conduct.md.md). Please follow it in all your interactions with the project.

### Issue/Bug Request

 **If you are having an issue with the existing project code, please submit a bug report under the following guidelines:**
 - Check first to see if your issue has already been reported.
 - Check to see if the issue has recently been fixed by attempting to reproduce the issue using the latest master branch in the repository.
 - Create a live example of the problem.
 - Submit a detailed bug report including your environment & browser, steps to reproduce the issue, actual and expected outcomes,  where you believe the issue is originating from, and any potential solutions you have considered.

### Feature Requests

We would love to hear from you about new features which would improve this app and further the aims of our project. Please provide as much detail and information as possible to show us why you think your new feature should be implemented.

### Pull Requests

If you have developed a patch, bug fix, or new feature that would improve this app, please submit a pull request. It is best to communicate your ideas with the developers first before investing a great deal of time into a pull request to ensure that it will mesh smoothly with the project.

Remember that this project is licensed under the MIT license, and by submitting a pull request, you agree that your work will be, too.

#### Pull Request Guidelines

- Ensure any install or build dependencies are removed before the end of the layer when doing a build.
- Update the README.md with details of changes to the interface, including new plist variables, exposed ports, useful file locations and container parameters.
- Ensure that your code conforms to our existing code conventions and test coverage.
- Include the relevant issue number, if applicable.
- You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.

### Attribution

These contribution guidelines have been adapted from [this good-Contributing.md-template](https://gist.github.com/PurpleBooth/b24679402957c63ec426).

## Project Overview

https://github.com/Lambda-School-Labs/Job-Funnel-ds-API/tree/master/docs

[Trello Board](https://trello.com/b/dorhqi4o/job-funnel)

[Product Canvas](https://www.notion.so/Job-Funnel-20ba287fac1c403c92a8ebb8766821a0)

[UX Design files](https://www.figma.com/file/zljtkyosMyzAa1UMpcAIEd/Quick-Hire-Judy?node-id=263%3A2)

## Template Link for this README

https://github.com/sfbrigade/data-science-wg/blob/master/dswg_project_resources/Project-README-template.md

[Backend Documentation](https://github.com/Lambda-School-Labs/Job-Funnel-be)

[Data Science Repo](https://github.com/Lambda-School-Labs/Job-Funnel-ds-API)
