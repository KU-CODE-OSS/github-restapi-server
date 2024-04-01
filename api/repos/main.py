from fastapi import APIRouter
from settings import *
from fastapi import Response
import httpx
import json

router = APIRouter(
    prefix="/api/repos",
    tags=['/api/repos'],
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
    student = json.loads(json_str)
    return student, json_str

@router.get('', response_class = Response)
async def get(github_id: str, repo_name: str):
    userinfo, j = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    print(userinfo)
    # item = {
    #     'created_at': userinfo["updated_at"]
    # }
    return j