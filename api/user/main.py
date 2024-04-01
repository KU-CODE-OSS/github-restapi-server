from fastapi import APIRouter
from settings import *
from fastapi import Response
import httpx
import json

router = APIRouter(
    prefix="/api/user",
    tags=['/api/user'],
)

async def request(url, header):
    r = httpx.get(url,headers=header)
    return r.json()

async def callGithubAPIUser(github_id):
    token = get_github_token()
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
    }
    url= f'{API_URL}/users/{github_id}'
    result = await request(url,headers)
    json_str = json.dumps(result, indent=4, default=str)
    student = json.loads(json_str)
    return student, json_str

async def callGithubAPI(suffix_URL, github_id):
    token = get_github_token()
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
    }
    url= f'{API_URL}/users/{github_id}/{suffix_URL}'
    result = await request(url,headers)
    json_str = json.dumps(result, indent=4, default=str)
    student = json.loads(json_str)
    return student, json_str

@router.get('/id', response_class = Response)
async def get(github_id: str):
    userinfo, j = await callGithubAPIUser(github_id=github_id)
    item = {
        'id': userinfo["id"]
    }
    return json.dumps(item)

@router.get('/node_id', response_class = Response)
async def get(github_id: str):
    userinfo = await callGithubAPIUser(github_id=github_id)
    item = {
        'node_id': userinfo["node_id"]
    }
    return json.dumps(item)

@router.get('/node_id', response_class = Response)
async def get(github_id: str):
    userinfo = await callGithubAPIUser(github_id=github_id)
    item = {
        'node_id': userinfo["node_id"]
    }
    return json.dumps(item)

@router.get('/avatar_url', response_class = Response)
async def get(github_id: str):
    userinfo = await callGithubAPIUser(github_id=github_id)
    item = {
        'avatar_url': userinfo["avatar_url"]
    }
    return json.dumps(item)

@router.get('/follower_list', response_class = Response)
async def get(github_id: str):
    page = 1
    id_list = []
    while True:
        follower_list = await callGithubAPI(f'followers?q=&page={page}&per_page=10', github_id=github_id)
        if follower_list[0] == 0:
            break
        
        for key in follower_list[0]:
            user = {
                'login': key['login'],
                'id' : key['id']
            }
            id_list.append(user)
        print(len(id_list))
        page += 1
    return json.dumps(id_list)

@router.get('/following_list', response_class = Response)
async def get(github_id: str):
    follower_list = await callGithubAPI('following?q=&page=1&per_page=100', github_id=github_id)

    id_list = []
    for key in follower_list[0]:
        user = {
            'login': key['login'],
            'id' : key['id']
        }
        id_list.append(user)
    return json.dumps(id_list)

@router.get('', response_class = Response)
async def get(github_id: str):
    GithubID = github_id

    student, json_str = await callGithubAPIUser(GithubID)
    
    user_item = {
        'GithubID': student['login'],
        'Follower_CNT': student['followers'],
        'Following_CNT': student['following'],
        'Public_repos_CNT': student['public_repos'],
        'Github_profile_Create_Date': student['created_at'],
        'Github_profile_Update_Date': student['updated_at'],
        #'email': student['email'],
        # 'Crawled_Date': datetime.now().strftime("%Y%m%d_%H%M%S")
    }
    return json_str
    return json.dumps(user_item)