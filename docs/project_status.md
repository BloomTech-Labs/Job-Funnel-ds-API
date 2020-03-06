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
