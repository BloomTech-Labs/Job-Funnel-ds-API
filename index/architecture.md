# Architecture Reference

## 1. Table of Contents
<!-- TOC -->

- [1. Table of Contents](#1-table-of-contents)
- [2. The Database](#2-the-database)
- [3. The ds-Data repo](#3-the-ds-data-repo)
	- [3.1. Populator](#31-populator)
		- [3.1.1. Running Populators](#311-running-populators)
	- [3.2. Scrapers](#32-scrapers)
	- [3.3. Models](#33-models)
	- [3.4. Hosting](#34-hosting)
	- [3.5. Utility API](#35-utility-api)
	- [3.6. Scheduled Runs](#36-scheduled-runs)
- [4. The ds-API repo](#4-the-ds-api-repo)

<!-- /TOC -->

## 2. The Database

The database (PostgreSQL) is hosted on AWS RDS (`database-1`). A summary of the structure can be found at `docs/db_structure/db_structure.md`, and schema details at `docs/db_structure/awsrds.schema`.

## 3. The ds-Data repo

The [ds-Data repo](https://github.com/Lambda-School-Labs/Job-Funnel-ds-Data) provides data aggregation (scrapers), pipelining (cleaning, deduplication and database access, built into the scrapers), and modeling. An ElasticBeanstalk instance hosts the `dev` branch.

### 3.1. Populator

The _Populator_ is defined in `ds-Data` at `datafunctions/populate.py`. It has two crucial methods, _retrieve\_and\_save\_data_ and _model\_and\_save\_topics_.

_retrieve\_and\_save\_data_ iterates through each scraper that is a subclass of _DataRetriever_, running each one's _get\_and\_store\_data_ method.

_model\_and\_save\_topics_ iterates through each model that is a subclass of _TopicModel_, running each one's _populate\_database_ method.

#### 3.1.1. Running Populators

Two utility scripts (`run_scrapers.py` and `run_models.py`) are provided, to initialize a _Populator_ and run _retrieve\_and\_save\_data_ and _model\_and\_save\_topics_, respectively. These scripts are what the `ds-Data` Utility API run (then disown) to start the scrapers and models.

### 3.2. Scrapers

Scrapers live in `ds-Data` at `datafunctions/retrieve/retrievers`. Each retriever *MUST* subclass the _DataRetriever_ base class (`datafunctions/retrieve/retrieverfunctions.py:DataRetriever`) and implement the _get\_and\_store\_data_ method (the _get\_data_ method was planned as an alternative in which the _Populator_ performs deduplication and database access, but was not fully implemented).


You can double check the Utility API for the scrapers at http://quickhire-api-dev.j535vysrhe.us-east-1.elasticbeanstalk.com/. If you ever want to double check everything is running properly, check:
http://quickhire-api-dev.j535vysrhe.us-east-1.elasticbeanstalk.com/health
http://quickhire-api-dev.j535vysrhe.us-east-1.elasticbeanstalk.com/logs?file=application.py


### 3.3. Models

Models live in `ds-Data` at `datafunctions/model/models`. Each retriever *MUST* subclass the _TopicModel_ base class (`datafunctions/model/modelfunctions.py:TopicModel`) and implement the _model\_and\_save\_topics_ method. This method should also update any additional model files (for example, NearestNeighbors or similar) that will be provided to the `ds-API`.

### 3.4. Hosting


The `ds-Data/dev` branch is hosted on Amazon Elastic Beanstalk, under app `quickhire`, environment `Quickhire-data-dev`.


`ds-API/dev` is on Elastic Beanstalk, `quickhire`, `Quickhire-API-dev`.

Both are deployed with a CodePipeline. (NOTE: The `quickhire-api-dev` CodePipeline does not automatically pull changes from GitHub. You have to manually release changes.)

### 3.5. Utility API

The Utility API can be found in `ds-Data` at `app.py` and provides control and monitoring functionality for the scrapers.


The following endpoints are available:
- Health check: /health
- Start scrapers: /start
	- NOTE: This starts the scrapers in a separate process then disowns that process, as otherwise the scrapers will get timed out.
- Kill scrapers: /kill
- Start models: /start-models
	- NOTE: This starts the models in a separate process then disowns that process, as otherwise the models might get timed out.
- Kill models: /kill-models
- app logs: /logs?file=app.py
- Scraper logs: /logs?file=run_scrapers.py
- Model logs: /logs?file=run_models.py

### 3.6. Scheduled Runs

Runs of the scrapers are initiated by a Lambda function that is scheduled every 12 hours. This function can be found at `docs/lambda/quickhire-data-dev-starter/lambda_function.py`, and calls the `/start` endpoint of the Utility API.

Runs of the models are initiated by a Lambda function that is scheduled every 7 minutes. This function can be found at `docs/lambda/quickhire-data-dev-starter-models/lambda_function.py`, and calls the `/start-models` endpoint of the Utility API.

## 4. The ds-API repo

The [ds-API repo](https://github.com/Lambda-School-Labs/Job-Funnel-ds-Data) provides an API for the web team to hit for searches, filtering, and other database access. In the future, it should use the models from `ds-Data` to provide strong keyword searches and matching of jobs vs user profile skills.

API documentation may be found at [docs/api/reference.md](../docs/api/reference.md)
