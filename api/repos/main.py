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
    response = json.loads(json_str)
    return response

# -------------------- Get all Data ------------------------------#
@router.get('', response_class=Response)
async def get(github_id: str, repo_name: str):

    repo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)

    #commits = await callGithubAPI(suffix_URL=f'{repo_name}/commits', github_id=github_id)
    #commit_count = len(commits)

    #closed_issues = await callGithubAPI(suffix_URL=f'{repo_name}/issues?state=closed', github_id=github_id)
    #closed_issue_count = len(closed_issues)

    languages = await callGithubAPI(suffix_URL=f'{repo_name}/languages', github_id=github_id)
    language_list = list(languages.keys())

    contributors = await callGithubAPI(suffix_URL=f'{repo_name}/contributors', github_id=github_id)
    contributor_logins = [contributor['login'] for contributor in contributors]

    readme = await callGithubAPI(suffix_URL=f'{repo_name}/readme', github_id=github_id)
    has_readme = True if readme else False

    latest_release = await callGithubAPI(suffix_URL=f'{repo_name}/releases/latest', github_id=github_id)
    release_version = latest_release.get('tag_name', 'No release')

    repo_item = {
        'id': repo["id"],
        'name': repo["name"],
        'url': repo["html_url"],
        'owner_github_id': repo["owner"]["login"],
        'created_at': repo["created_at"],
        'updated_at': repo["updated_at"],
        'forks_count': repo["forks_count"],
        'stars_count': repo["stargazers_count"],
        #'commit_count': commit_count,
        #'open_issue_count': repo["open_issues_count"],
        #'closed_issue_count': closed_issue_count,
        'language': language_list,
        'contributors': contributor_logins,
        'license': repo["license"]["name"],
        'has_readme': has_readme,
        'description': repo["description"],
        'release_version': release_version
    }

    return response(repo_item)
#----------------------------------------------------------------#

#--------------------- Get data individually --------------------#
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

@router.get('/html_url', response_class = Response)
async def get(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    item = {
        'owner': repoinfo["html_url"]
    }
    return response(item)

@router.get('/owner', response_class = Response)
async def get(github_id: str, repo_name: str):
    item = {
        'owner': github_id
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

@router.get('/commit_count', response_class=Response)
async def get(github_id: str, repo_name: str):
    commit_count = 0
    page = 1
    while True:
        commits = await callGithubAPI(suffix_URL=f"{repo_name}/commits?q=&page={page}&per_page=100", github_id=github_id)
        if not commits:
            break
        
        commit_count += len(commits)
        page += 1
        print(commit_count)

    item = {
        'commit_count': commit_count
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

@router.get('/closed_issues_count', response_class=Response)
async def get(github_id: str, repo_name: str):
    closed_issues_count = 0
    page = 1
    while True:
        closed_issues = await callGithubAPI(suffix_URL=f"{repo_name}/issues?state=closed&page={page}&per_page=100", github_id=github_id)
        if not closed_issues:         
            break
        
        closed_issues_count += len(closed_issues)   
        page += 1  

    item = {
        'closed_issues_count': closed_issues_count
    }
    return response(item)

@router.get('/laguages', response_class=Response)
async def get(github_id: str, repo_name: str):
    languages = await callGithubAPI(suffix_URL=f"{repo_name}/languages", github_id=github_id)

    language_names = list(languages.keys())

    item = {
        'languages': language_names
    }
    return response(item)

@router.get('/contributors', response_class=Response)
async def get(github_id: str, repo_name: str):
    countributors = await callGithubAPI(suffix_URL=f"{repo_name}/contributors", github_id=github_id)

    contributors_names = [contributor['login'] for contributor in countributors]

    item = {
        'contributor': contributors_names
    }
    return response(item)

@router.get('/license', response_class=Response)
async def get(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    item = {
        'license': repoinfo["license"]["key"]
    }
    return response(item)

@router.get('/has_readme', response_class=Response)
async def get(github_id: str, repo_name: str):
    try:
        readme_info = await callGithubAPI(suffix_URL=f"{repo_name}/readme", github_id=github_id)
        has_readme = True if readme_info else False
    except Exception as e:
        has_readme = False

    item = {
        'has_readme': has_readme
    }
    return response(item)

@router.get('/discription', response_class=Response)
async def get(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    item = {
        'description' : repoinfo["description"]
    }
    return response(item)

@router.get('/release_version', response_class=Response)
async def get(github_id: str, repo_name: str):
    try:
        latest_release = await callGithubAPI(suffix_URL=f"{repo_name}/releases/latest", github_id=github_id)
        release_version = latest_release['tag_name'] if latest_release else 'No release found'
    except Exception as e:
        release_version = 'No release found'

    item = {
        'release_version': release_version
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
# ---------------------------------------------------------------#