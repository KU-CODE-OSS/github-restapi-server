from fastapi import APIRouter
from settings import *
from fastapi import Response
import httpx
import json

router = APIRouter(
    prefix="/api/repos/pulls",
    tags=['/api/repos/pulls'],
)

async def request(url, header):
    r = httpx.get(url,headers=header)
    return r.json()

async def callGithubAPI(suffix_URL, github_id):
    token = get_github_token()
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
    }
    url= f'{API_URL}/repos/{github_id}/{suffix_URL}'
    result = await request(url,headers)
    json_str = json.dumps(result, indent=4, default=str)
    response = json.loads(json_str)
    return response

# -------------------- Get all Data ------------------------------#
@router.get('', response_class = Response)
async def get(github_id: str, repo_name: str):
    pulls = []
    states = ['open', 'closed'] 

    for state in states:
        page = 1  
        while True:
            pull_list = await callGithubAPI(f'{repo_name}/pulls?q=&state={state}&page={page}&per_page=100', github_id=github_id)
            if not pull_list:  
                break

            for pull in pull_list:
                pull_data = {
                    'id': pull["id"],
                    'owner_github_id' : f'{github_id}',
                    'state': pull["state"],
                    'title': pull["title"],
                    'repo_url' : f'{HTML_URL}/{github_id}/{repo_name}',
                    'requester_id': pull['user']['login'],
                }
                pulls.append(pull_data)
            page += 1  
    return response(pulls)        
#----------------------------------------------------------------#

#--------------------- Get data individually --------------------#
@router.get('/open', response_class=Response)
async def get_issues(github_id: str, repo_name: str):
    page = 1
    pulls = []
    while True:
        pulls_list = await callGithubAPI(f'{repo_name}/pulls?q=&state=open&page={page}&per_page=100', github_id=github_id)
        if len(pulls_list) == 0:
            break

        for pull in pulls_list:
            pull_data = {
                'id': pull["id"],
                'owner_github_id' : f'{github_id}',
                'state': pull["state"],
                'title': pull["title"],
                'repo_url' : f'{HTML_URL}/{github_id}/{repo_name}',
                'requester_id': pull['user']['login'],
            }
            pulls.append(pull_data)
        page += 1
    return response(pulls)

@router.get('/closed', response_class=Response)
async def get_issues(github_id: str, repo_name: str):
    page = 1
    pulls = []
    while True:
        pull_list = await callGithubAPI(f'{repo_name}/pulls?sate=closed&page={page}&per_page=100', github_id=github_id)
        if len(pull_list) == 0:
            break

        for pull in pull_list:
            pull_data = {
                'id': pull["id"],
                'owner_github_id' : f'{github_id}',
                'state': pull["state"],
                'title': pull["title"],
                'repo_url' : f'{HTML_URL}/{github_id}/{repo_name}',
                'requester_id': pull['user']['login']
            }
            pulls.append(pull_data)
        page += 1
    return response(pulls)
#----------------------------------------------------------------#
