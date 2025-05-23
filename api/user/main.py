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
async def call_github_api_user(github_id):
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
async def call_github_api_user_repo(suffix_url, github_id):
    global remaining_requests, current_token
    
    if remaining_requests <= 0 or current_token is None:
        current_token = await get_new_token()
    
    headers = {
        'Authorization': f'token {current_token}',
        'Accept': 'application/vnd.github.v3+json',
    }
    url = f'{API_URL}/users/{github_id}/{suffix_url}'
    
    return await request(url, headers)
# ------------------------ #

# --- Get all data --- #
@router.get('', response_class=Response)
async def get(github_id: str):
    github_user_id = github_id

    # Call the GitHub API and fetch user data
    await asyncio.sleep(REQ_DELAY)
    student_data = await call_github_api_user(github_user_id)

    if 'error' in student_data:
        print(f"Error encountered: {student_data['error']}")
        raise HTTPException(status_code=404, detail=f"User {github_user_id} not found")
    
    # Use .get() to safely access keys and allow None values
    user_data = {
        'github_id': student_data.get('login'),
        'follower_count': student_data.get('followers'),
        'following_count': student_data.get('following'),
        'public_repos_count': student_data.get('public_repos'),
        'github_profile_create_date': student_data.get('created_at'),
        'github_profile_update_date': student_data.get('updated_at'),
        'email': student_data.get('email'),
        'crawled_date': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    }

    # Replace any None values with "null" (this step is redundant for JSON serialization in Python but included for clarity)
    user_data = {k: (v if v is not None else None) for k, v in user_data.items()}

    print("-" * 20)
    print("api/user")
    print(user_data)
    
    return Response(content=json.dumps(user_data), media_type='application/json')
# ---------------------------------------------------------------#

# --- Get User's Repo id, name--- #
@router.get('/repos', response_class=Response)
async def get_repos(github_id: str):
    page = 1
    repositories = []
    per_page = 100

    while True:
        await asyncio.sleep(REQ_DELAY)
        repository_list = await call_github_api_user_repo(f'repos?q=&page={page}&per_page={per_page}', github_id=github_id)
        if not repository_list:
            break

        for repo in repository_list:
            # Only include public repositories and ensure all data fields are safe
            if not repo.get('private', True):
                repository_data = {
                    'id': repo.get('id'),
                    'name': repo.get('name'),
                    'full_name': repo.get('full_name')
                }
                repositories.append(repository_data)

        # If the number of repos fetched is less than per_page, break out of loop as there are no more
        if len(repository_list) < per_page:
            break

        page += 1

    print("-" * 20)
    print("api/user/repos")
    print(f"Total repos: {len(repositories)}")
    return Response(content=json.dumps(repositories), media_type='application/json')