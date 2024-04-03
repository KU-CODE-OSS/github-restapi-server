from fastapi import APIRouter
from settings import *
from fastapi import Response
import httpx
import json

router = APIRouter(
    prefix="/api/contributor",
    tags=['/api/contributor'],
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
    url= f'{API_URL}/repos/{github_id}/{suffix_URL}/contributors'
    result = await request(url,headers)
    json_str = json.dumps(result, indent=4, default=str)
    response = json.loads(json_str)
    return response

# -------------------- Get all Data ------------------------------#
@router.get('', response_class = Response)
async def get(github_id: str, repo_name: str):

    contributors = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)

    contributors_list = [
        {
            'repo_url' : f'{HTML_URL}/{github_id}/{repo_name}',
            'login': contributor["login"], 
            'contributions': contributor["contributions"]} for contributor in contributors
    ]
    return response(contributors_list)
#----------------------------------------------------------------#