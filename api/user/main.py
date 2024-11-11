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
    await asyncio.sleep(REQ_DELAY)
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
    print(user_item)

    return Response(content=json.dumps(user_item), media_type='application/json')
# ---------------------------------------------------------------#

# --- Get User's Repo id, name--- #
@router.get('/repos', response_class=Response)
async def get(github_id: str):
    page = 1
    repos = []
    per_page = 100
    
    while True:
        await asyncio.sleep(REQ_DELAY)
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
    
    print(f"Total repos: {len(repos)}")
    print(repos)
    return Response(content=json.dumps(repos), media_type='application/json')
