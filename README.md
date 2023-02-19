# Transport Route Planner
This repository will contain an API which will allow a consumer of the API to obtain the time of arrival at a particular train destination given a list of train stations the user wishes to traverse. 

### Pre-requisites
When running using Docker:
* Docker with version >= 20.10.11 (could work for earlier versions but not tested)
* Docker-Compose version >= 1.29.2 (could work for earlier versions but not tested)

When running locally:
* python3.9 or above 
* sqlite 3

### Stack 
The API will be using python 3.9 and utilising the FastAPI framework, advantage of using FastAPI instead of Flask or Django is that the API docs are auto generated if defined using best practices. The database will be an sqlite 3 instance. 

## How to run

### Environment Variables
Before running please define following environment variables in your terminal of choice: 
* APP_ID - transport API app_id
* APP_KEY - transport API app_key
* TRANSPORT_DOMAIN - transport API domain, default value is `https://transportapi.com`

#### Docker
If your machine has the pre-requisites installed, to run the application, from the root folder of the repository run:
```docker-compose up```

To test it you can run `curl localhost:8000/` and if the response is `{"Test": "Success"}` then you have successfully set up the repository locally. 

#### Locally
If you would prefer to run the files locally, please follow these steps:
1. First create virtual environment by running `python3 -m venv ./venv`
2. Run `source venv/bin/activate`
3. From root of repository run `pip3 install -r requirements.txt`
4. From root of repository run `python3 -m uvicorn app.run:app --host 0.0.0.0 --port 8000 --reload`

To test it you can run `curl localhost:8000/` and if the response is `{"Test": "Success"}` then you have successfully set up the repository locally. 

### Documentation
Once the repository is successfully set up locally, documentation can be accessed on:
* `http://localhost:8000/redoc` to obtain OpenAPI3.0 compliant specification for the API's this repository is supporting. 
* `http://localhost:8000/docs` to obtain OpenAPI3.0 swagger client which will allow for test calls to each endpoint