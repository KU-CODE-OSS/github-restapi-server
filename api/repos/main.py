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
    return student

@router.get('', response_class = Response)
async def get(github_id: str, repo_name: str):

    repo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    return response(repo)

@router.get('/id', response_class = Response)
async def get(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    item = {
        'id': repoinfo["id"]
    }
    return response(item)

@router.get('/node_id', response_class = Response)
async def get(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    item = {
        'node_id': repoinfo["node_id"]
    }
    return response(item)

@router.get('/name', response_class = Response)
async def get(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    item = {
        'name': repoinfo["name"]
    }
    return response(item)

@router.get('/full_name', response_class = Response)
async def get(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    item = {
        'full_name': repoinfo["full_name"]
    }
    return response(item)

@router.get('/created_at', response_class = Response)
async def get(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    item = {
        'created_at': repoinfo["created_at"]
    }
    return response(item)

@router.get('/updated_at', response_class = Response)
async def get(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    item = {
        'updated_at': repoinfo["updated_at"]
    }
    return response(item)

@router.get('/pushed_at', response_class = Response)
async def get(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    item = {
        'pushed_at': repoinfo["pushed_at"]
    }
    return response(item)

@router.get('/clone', response_class = Response)
async def get(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    item = {
        'https': repoinfo["clone_url"],
        'ssh': repoinfo["ssh_url"]
    }
    return response(item)

@router.get('/stars_count', response_class = Response)
async def get(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    item = {
        'stars': repoinfo["stargazers_count"]
    }
    return response(item)

@router.get('/watchers_count', response_class = Response)
async def get(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    item = {
        'watchers': repoinfo["watchers"]
    }
    return response(item)

@router.get('/repo_size', response_class = Response)
async def get(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    item = {
        'size': repoinfo["size"]
    }
    return response(item)

@router.get('/forks_count', response_class = Response)
async def get(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    item = {
        'forks': repoinfo["forks"]
    }
    return response(item)

@router.get('/open_issues_count', response_class = Response)
async def get(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    item = {
        'open_issues_count': repoinfo["open_issues_count"]
    }
    return response(item)

@router.get('/fork', response_class = Response)
async def get(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    item = {
        'fork': repoinfo["fork"]
    }
    return response(item)

@router.get('/fork_users', response_class = Response)
async def get(github_id: str, repo_name: str):
    page = 1
    user_list = []
    while True:
        users = await callGithubAPI(suffix_URL=f'{repo_name}/forks?q=&page={page}&per_page=100', github_id=github_id)
        if len(users) == 0:
            break

        for key in users:
            d = {}
            d['github_id'] = key['owner']['login']
            d['id'] = key['owner']['id']
            d['url'] = key['owner']['url']
            user = {
                'owner' : d,
                'id' : key['id'],
                'name': key['name'],
                'full_name': key['full_name'],
                'stars': key['stargazers_count'],
                'watchers': key["watchers"],
                'forks': key["forks"],
                'open_issues_count': key['open_issues_count'],
            }
            user_list.append(user)
        page += 1
    return response(user_list)
    