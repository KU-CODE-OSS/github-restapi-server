from fastapi import APIRouter
from settings import *
from fastapi import Response
import httpx
import json

router = APIRouter(
    prefix="/api/repos/issue",
    tags=['/api/repos/issue'],
)

async def request(url, header):
    r = httpx.get(url,headers=header)
    return r.json()

async def callGithubAPI_ISSUE(suffix_URL, github_id):
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
    issues = []
    states = ['open', 'closed'] 

    for state in states:
        page = 1  
        while True:
            issue_list = await callGithubAPI_ISSUE(f'{repo_name}/issues?q=&state={state}&page={page}&per_page=100', github_id=github_id)
            print(page)
            if not issue_list:  
                break

            for issue in issue_list:
                issue_data = {
                    'id': issue['id'],
                    'owner_github_id': github_id,
                    'repo_url': f'{HTML_URL}/{github_id}/{repo_name}',
                    'state': issue['state'],
                    'title': issue['title'],
                    'publisher_github_id': issue['user']['login'] if issue['user'] else 'Unknown',  
                }
                issues.append(issue_data)
            page += 1  
            
    return response(issues)
#----------------------------------------------------------------#

#--------------------- Get data individually --------------------#
@router.get('/open', response_class=Response)
async def get_issues(github_id: str, repo_name: str):
    page = 1
    issues = []
    while True:
        issue_list = await callGithubAPI_ISSUE(f'{repo_name}/issues?q=&state=open&page={page}&per_page=100', github_id=github_id)
        if len(issue_list) == 0:
            break

        for issue in issue_list:
            issue_data = {
                'id': issue['id'],
                'owner_github_id' : f'{github_id}',
                'repo_url' : f'{HTML_URL}/{github_id}/{repo_name}',
                'state': issue['state'],
                'title': issue['title'],
                'publisher_github_id': issue['user']['login'],
            }
            issues.append(issue_data)
        page += 1
        print(page)
    return response(issues)

@router.get('/closed', response_class=Response)
async def get_issues(github_id: str, repo_name: str):
    page = 1
    issues = []
    while True:
        issue_list = await callGithubAPI_ISSUE(f'{repo_name}/issues?q=&state=closed&page={page}&per_page=100', github_id=github_id)
        if len(issue_list) == 0:
            break

        for issue in issue_list:
            issue_data = {
                'id': issue['id'],
                'owner_github_id' : f'{github_id}',
                'repo_url' : f'{HTML_URL}/{github_id}/{repo_name}',
                'state': issue['state'],
                'title': issue['title'],
                'publisher_github_id': issue['user']['login'],
            }
            issues.append(issue_data)
        page += 1
        print(page)
    return response(issues)
#----------------------------------------------------------------#