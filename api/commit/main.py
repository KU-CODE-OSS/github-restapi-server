from fastapi import APIRouter
from settings import *
from fastapi import Response
import httpx
import json

router = APIRouter(
    prefix="/api/commit",
    tags=['/api/commit'],
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
    url= f'{API_URL}/repos/{github_id}/{suffix_URL}/commits'
    result = await request(url,headers)
    json_str = json.dumps(result, indent=4, default=str)
    response = json.loads(json_str)
    return response

# -------------------- Get all Data ------------------------------#
@router.get('', response_class = Response)
async def get(github_id: str, repo_name: str):
    page = 1
    commits = []
    while True:
        commit_list = await callGithubAPI(f'{repo_name}/commits?q=&page={page}&per_page=100', github_id=github_id)
        if len(commit_list) == 0:
            break

        for commit in commit_list:
            sha = commit["sha"]
            commit_detail = await callGithubAPI(f'{repo_name}/commits/{sha}', github_id=github_id)
            commit_data = {
                'id': sha,
                'repo_url': f'{HTML_URL}/{github_id}/{repo_name}',
                'owner_github_id': github_id,
                'committer_github_id': commit['commit']['author']['name'],  # Sometimes 'author' can be null
                'added_lines': commit_detail['stats']['additions'],
                'deleted_lines': commit_detail['stats']['deletions']
            }
            commits.append(commit_data)
        page += 1
    return response(commits)
#-----------------------------------------------------------------#