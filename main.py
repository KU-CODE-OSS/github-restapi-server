import httpx
import json
from datetime import datetime
from multiprocessing import Process

# --- FAST API ---#
from fastapi import Response
from fastapi import FastAPI
from api.user import main
# --- settings --- #
from settings import *

app = FastAPI()
app.include_router(main.router)

#-------------- ROOT ---------------------#
@app.get("/home")
async def root():

    return {"message": "Welcome to the FastAPI application"}
#-----------------------------------------#


@app.get('/repo')
async def start_requests():
    token = get_github_token()
    
    GithubID = 'kdgyun'
    repoNM = 'k8s-cluster-bootstrap'

    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    url= f'{API_URL}/repos/{GithubID}/{repoNM}'

    result = await request(url,headers)
    json_str = json.dumps(result, indent=4, default=str)
    repo = json.loads(json_str)
    
    repo_item = {

        'RepoID' : repo['id'],
        'RepoURL' : repo['html_url'],
        'RepoNM' : repo['name'],
        'OwnerGithubID' : repo['owner']['login'],
        'CreationDate' : repo['created_at'],
        'ForkCount' : repo['forks_count'],
        'StarCount' : repo['stargazers_count'],
        'OpenIssueCount' : repo['open_issues_count'],
        'LicenseName' : repo['license'],
        'ProjectDescription' : repo['description'],
        'ProgrammingLanguage' : None,
        'Contributors' : None,
        'CommitCount' : None,
        'HasReadME' : None,
        'ReleaseVersion' : None
    }   

    return repo_item
