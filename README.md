# github-restapi-server
## prerequisite
```
pip3 install virtualenv
```
### CREATE GITHUB_TOKEN file and Add AUTH TOKEN

## Setup and Usage
Before starting FASTAPI server, make venv and download requirements in github-restapi-server 
```
virtualenv {venv_name}
```
```
source {venv_name}/bin/activate
```
```
pip3 install -r requirements.txt
```

## MAKE GITHUB_TOKEN file and put Auth Token

## Start FASTAPI Server
```
nohup uvicorn main:app --reload --host 0.0.0.0 --port 5000 --timeout-keep-alive 30 > uvicorn.log 2>&1 &
```