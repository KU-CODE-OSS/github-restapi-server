from fastapi import APIRouter
from settings import *
from fastapi import Response
import httpx
import json

router = APIRouter(
    prefix="/api/pr",
    tags=['/api/pr'],
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
    url= f'{API_URL}/repos/{github_id}/{suffix_URL}/pulls'
    result = await request(url,headers)
    json_str = json.dumps(result, indent=4, default=str)
    student = json.loads(json_str)
    return student

@router.get('', response_class = Response)
async def get(github_id: str, repo_name: str):

    prs = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    return response(prs)

@router.get('/open', response_class=Response)
async def get_issues(github_id: str, repo_name: str):
    page = 1
    prs = []
    while True:
        pr_list = await callGithubAPI(f'{repo_name}/pulls?sate=open&page={page}&per_page=100', github_id=github_id)
        if len(pr_list) == 0:
            break

        for pr in pr_list:
            pr_data = {
                'id': pr["id"],
                'owner_github_id' : f'{github_id}',
                'state': pr["state"],
                'title': pr["title"],
                'repo_url' : f'{HTML_URL}/{github_id}/{repo_name}',
                'requester_id': pr['user']['login'],
            }
            prs.append(pr_data)
        page += 1
    return response(prs)

@router.get('/closed', response_class=Response)
async def get_issues(github_id: str, repo_name: str):
    page = 1
    prs = []
    while True:
        pr_list = await callGithubAPI(f'{repo_name}/pulls?sate=closed&page={page}&per_page=100', github_id=github_id)
        if len(pr_list) == 0:
            break

        for pr in pr_list:
            pr_data = {
                'id': pr["id"],
                'owner_github_id' : f'{github_id}',
                'state': pr["state"],
                'title': pr["title"],
                'repo_url' : f'{HTML_URL}/{github_id}/{repo_name}',
                'requester_id': pr['user']['login']
            }
            prs.append(pr_data)
        page += 1
    return response(prs)