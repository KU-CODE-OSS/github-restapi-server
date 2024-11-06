from fastapi import APIRouter, Response, HTTPException

from utils.settings import *
from commons.api_client import request

import httpx
import json
from datetime import datetime

router = APIRouter(
    prefix="/api/user",
    tags=['/api/user'],
)

# --- Call GitHub API to fetch user data --- #
async def callGithubAPIUser(github_id):
    global remaining_requests, current_token
    
    if remaining_requests <= 0 or current_token is None:
        current_token = await get_new_token()
    
    headers = {
        'Authorization': f'token {current_token}',
        'Accept': 'application/vnd.github.v3+json',
    }
    
    url = f'{API_URL}/users/{github_id}'
    return await request(url, headers)
# ------------------------ #

# --- Call GitHub API with a suffix URL --- #
async def callGithubAPIUserRepo(suffix_URL, github_id):
    global remaining_requests, current_token
    
    if remaining_requests <= 0 or current_token is None:
        current_token = await get_new_token()
    
    headers = {
        'Authorization': f'token {current_token}',
        'Accept': 'application/vnd.github.v3+json',
    }
    url= f'{API_URL}/users/{github_id}/{suffix_URL}'
    
    return await request(url, headers)
# ------------------------ #

# --- Get all data --- #
@router.get('', response_class=Response)
async def get(github_id: str):
    GithubID = github_id

    # Call the GitHub API and fetch user data
    student = await callGithubAPIUser(GithubID)

    if 'error' in student:
        print(f"Error encountered: {student['error']}")
        raise HTTPException(status_code=404, detail=f"User {GithubID} not found")
    
    user_item = {
        'GithubID': student['login'],
        'Follower_CNT': student['followers'],
        'Following_CNT': student['following'],
        'Public_repos_CNT': student['public_repos'],
        'Github_profile_Create_Date': student['created_at'],
        'Github_profile_Update_Date': student['updated_at'],
        'email': student['email'],
        'crawled_date': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    }

    return Response(content=json.dumps(user_item), media_type='application/json')
# ---------------------------------------------------------------#

# # --- Get data individually --- #
# @router.get('/id', response_class=Response)
# async def get(github_id: str):
#     userinfo = await callGithubAPIUser(github_id=github_id)
#     item = {
#         'id': userinfo["id"]
#     }
#     return Response(content=json.dumps(item), media_type='application/json')


# @router.get('/node_id', response_class=Response)
# async def get(github_id: str):
#     userinfo = await callGithubAPIUser(github_id=github_id)
#     item = {
#         'node_id': userinfo["node_id"]
#     }
#     return Response(content=json.dumps(item), media_type='application/json')


# @router.get('/avatar_url', response_class=Response)
# async def get(github_id: str):
#     userinfo = await callGithubAPIUser(github_id=github_id)
#     item = {
#         'avatar_url': userinfo["avatar_url"]
#     }
#     return Response(content=json.dumps(item), media_type='application/json')


# @router.get('/follower_list', response_class=Response)
# async def get(github_id: str):
#     page = 1
#     id_list = []
#     while True:
#         follower_list = await callGithubAPI(f'followers?q=page={page}&per_page=100', github_id=github_id)
#         if len(follower_list) == 0:
#             break

#         for key in follower_list:
#             user = {
#                 'login': key['login'],
#                 'id': key['id']
#             }
#             id_list.append(user)
#         page += 1
#     return Response(content=json.dumps(id_list), media_type='application/json')


# @router.get('/followers', response_class=Response)
# async def get(github_id: str):
#     userinfo = await callGithubAPIUser(github_id=github_id)
#     item = {
#         'followers': userinfo["followers"]
#     }
#     return Response(content=json.dumps(item), media_type='application/json')


# @router.get('/following_list', response_class=Response)
# async def get(github_id: str):
#     page = 1
#     id_list = []
#     while True:
#         following_list = await callGithubAPI(f'following?q=page={page}&per_page=100', github_id=github_id)
#         if len(following_list) == 0:
#             break

#         for key in following_list:
#             user = {
#                 'login': key['login'],
#                 'id': key['id']
#             }
#             id_list.append(user)
#         page += 1
#     return Response(content=json.dumps(id_list), media_type='application/json')


# @router.get('/name', response_class=Response)
# async def get(github_id: str):
#     userinfo = await callGithubAPIUser(github_id=github_id)
#     item = {
#         'name': userinfo["name"]
#     }
#     return Response(content=json.dumps(item), media_type='application/json')


# @router.get('/public_repos', response_class=Response)
# async def get(github_id: str):
#     userinfo = await callGithubAPIUser(github_id=github_id)
#     item = {
#         'public_repos': userinfo["public_repos"]
#     }
#     return Response(content=json.dumps(item), media_type='application/json')


# @router.get('/repo_list', response_class=Response)
# async def get(github_id: str):
#     page = 1
#     id_list = []
#     while True:
#         repo_list = await callGithubAPI(f'repos?q=page={page}&per_page=100', github_id=github_id)
#         if len(repo_list) == 0:
#             break

#         for key in repo_list:
#             user = {
#                 'name': key['name'],
#                 'id': key['id'],
#                 'full_name': key['full_name']
#             }
#             id_list.append(user)
#         page += 1
#     return Response(content=json.dumps(id_list), media_type='application/json')


# @router.get('/public_gists', response_class=Response)
# async def get(github_id: str):
#     userinfo = await callGithubAPIUser(github_id=github_id)
#     item = {
#         'public_repos': userinfo["public_gists"]
#     }
#     return Response(content=json.dumps(item), media_type='application/json')


# @router.get('/created_at', response_class=Response)
# async def get(github_id: str):
#     userinfo = await callGithubAPIUser(github_id=github_id)
#     item = {
#         'created_at': userinfo["created_at"]
#     }
#     return Response(content=json.dumps(item), media_type='application/json')


# @router.get('/updated_at', response_class=Response)
# async def get(github_id: str):
#     userinfo = await callGithubAPIUser(github_id=github_id)
#     item = {
#         'created_at': userinfo["updated_at"]
#     }
#     return Response(content=json.dumps(item), media_type='application/json')


@router.get('/repos', response_class=Response)
async def get(github_id: str):
    page = 1
    repos = []
    per_page = 100
    
    while True:
        repo_list = await callGithubAPIUserRepo(f'repos?q=&page={page}&per_page={per_page}', github_id=github_id)
        if not repo_list:
            break

        for repo in repo_list:
            if not repo['private']:
                user = {
                    'id': repo['id'],
                    'name': repo['name'],
                    'full_name': repo['full_name'],
                }
                repos.append(user)
        
        if len(repo_list) < per_page:
            break

        page += 1

    return Response(content=json.dumps(repos), media_type='application/json')
