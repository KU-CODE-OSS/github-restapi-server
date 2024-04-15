from fastapi import APIRouter
from settings import *
from fastapi import Response
import httpx
from bs4 import BeautifulSoup
import json

# --- ROUTER ---#
router = APIRouter(
    prefix="/api/repos",
    tags=['/api/repos'],
)
# ------------- #

# --- REQUEST FUNCTIONS (API) ---#
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

async def callGithubAPI_CONTRIBUTOR(suffix_URL, github_id):
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

async def callGithubAPI_ISSUE(suffix_URL, github_id, state, page):
    token = get_github_token()
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
    }
    url= f'{API_URL}/repos/{github_id}/{suffix_URL}/issues?q=&state={state}&page={page}&per_page=100'
    result = await request(url,headers)
    json_str = json.dumps(result, indent=4, default=str)
    response = json.loads(json_str)
    return response

async def callGithubAPI_PULL(suffix_URL, github_id, state, page):
    token = get_github_token()
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
    }
    url= f'{API_URL}/repos/{github_id}/{suffix_URL}/pulls?q=&state={state}&page={page}&per_page=100'
    result = await request(url,headers)
    json_str = json.dumps(result, indent=4, default=str)
    response = json.loads(json_str)
    return response

async def callGithubAPI_COMMIT(suffix_URL, github_id, page):
    token = get_github_token()
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
    }
    url= f'{API_URL}/repos/{github_id}/{suffix_URL}/commits?q=&page={page}&per_page=100'
    result = await request(url,headers)
    json_str = json.dumps(result, indent=4, default=str)
    response = json.loads(json_str)
    return response

async def callGithubAPI_COMMIT_DETAIL(suffix_URL, github_id, sha):
    token = get_github_token()
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
    }
    url= f'{API_URL}/repos/{github_id}/{suffix_URL}/commits/{sha}'
    result = await request(url,headers)
    json_str = json.dumps(result, indent=4, default=str)
    response = json.loads(json_str)
    return response
# ------------------------ #

# -------------------- Get all Data ------------------------------#
@router.get('', response_class=Response)
async def get(github_id: str, repo_name: str):

    repo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)

    #commit_response = await callGithubHTTP(f'{repo_name}', github_id)
    #issue_response = await callGithubHTTP(f'{repo_name}/issues', github_id)

    #commit_count = BeautifulSoup(commit_response.content, 'html.parser').select_one(HTTP_COMMIT).get_text(strip=True).split()[0]
    #soup = BeautifulSoup(issue_response.content, 'html.parser')

    #open_issues_count = soup.select_one(HTTP_OPEN_ISSUE).get_text(strip=True).split()[0]
    #closed_issues_count = soup.select_one(HTTP_CLOSED_ISSUE).get_text(strip=True).split()[0]

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
        'commit_count': commit_count,
        'open_issue_count': open_issues_count,
        'closed_issue_count': closed_issues_count,
        'language': language_list,
        'contributors': contributor_logins,
        'license': repo["license"]["name"] if repo["license"] else None,
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

# -------------------- /repos/contributor ------------------------------#
@router.get('/contributor', response_class = Response)
async def get(github_id: str, repo_name: str):

    contributors = await callGithubAPI_CONTRIBUTOR(suffix_URL=repo_name, github_id=github_id)

    contributors_list = [
        {
            'repo_url' : f'{HTML_URL}/{github_id}/{repo_name}',
            'login': contributor["login"], 
            'contributions': contributor["contributions"]} for contributor in contributors
    ]
    return response(contributors_list)
#----------------------------------------------------------------#

# -------------------- /repos/issues ------------------------------#
@router.get('/issues', response_class = Response)
async def get(github_id: str, repo_name: str):
    issues = []
    states = ['open', 'closed'] 

    for state in states:
        page = 1  
        while True:
            issue_list = await callGithubAPI_ISSUE(suffix_URL=repo_name, github_id=github_id, state=state, page=page)
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

@router.get('/issues/open', response_class=Response)
async def get_issues(github_id: str, repo_name: str):
    page = 1
    issues = []
    state = "open"
    while True:
        issue_list = await callGithubAPI_ISSUE(suffix_URL=repo_name, github_id=github_id, state=state, page=page)
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
    return response(issues)

@router.get('/issues/closed', response_class=Response)
async def get_issues(github_id: str, repo_name: str):
    page = 1
    issues = []
    state = "closed"
    while True:
        issue_list = await callGithubAPI_ISSUE(suffix_URL=repo_name, github_id=github_id, state=state, page=page)
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
    return response(issues)
#----------------------------------------------------------------#

#-------------------- repos/pulls ------------------------------#
@router.get('/pulls', response_class = Response)
async def get(github_id: str, repo_name: str):
    pulls = []
    states = ['open', 'closed'] 

    for state in states:
        page = 1  
        while True:
            pull_list = await callGithubAPI_PULL(suffix_URL=repo_name, github_id=github_id, state=state, page=page)
            if not pull_list:  
                break

            for pull in pull_list:
                pull_data = {
                    'id': pull["id"],
                    'owner_github_id' : f'{github_id}',
                    'state': pull["state"],
                    'title': pull["title"],
                    'repo_url' : f'{HTML_URL}/{github_id}/{repo_name}',
                    'requester_id': pull['user']['login'],
                }
                pulls.append(pull_data)
            page += 1  
    return response(pulls)        

@router.get('/pulls/open', response_class=Response)
async def get_issues(github_id: str, repo_name: str):
    page = 1
    pulls = []
    state = "open"
    while True:
        pulls_list = await callGithubAPI_PULL(suffix_URL=repo_name, github_id=github_id, state=state, page=page)
        if len(pulls_list) == 0:
            break

        for pull in pulls_list:
            pull_data = {
                'id': pull["id"],
                'owner_github_id' : f'{github_id}',
                'state': pull["state"],
                'title': pull["title"],
                'repo_url' : f'{HTML_URL}/{github_id}/{repo_name}',
                'requester_id': pull['user']['login'],
            }
            pulls.append(pull_data)
        page += 1
    return response(pulls)

@router.get('/pulls/closed', response_class=Response)
async def get_issues(github_id: str, repo_name: str):
    page = 1
    pulls = []
    state = "closed"
    while True:
        pull_list = await callGithubAPI_PULL(suffix_URL=repo_name, github_id=github_id, state=state, page=page)
        if len(pull_list) == 0:
            break

        for pull in pull_list:
            pull_data = {
                'id': pull["id"],
                'owner_github_id' : f'{github_id}',
                'state': pull["state"],
                'title': pull["title"],
                'repo_url' : f'{HTML_URL}/{github_id}/{repo_name}',
                'requester_id': pull['user']['login']
            }
            pulls.append(pull_data)
        page += 1
    return response(pulls)
#----------------------------------------------------------------#

# -------------------- repos/commit ------------------------------#
@router.get('/commit', response_class = Response)
async def get(github_id: str, repo_name: str):
    page = 1
    commits = []
    while True:
        commit_list = await callGithubAPI_COMMIT(suffix_URL=repo_name, github_id=github_id, page=page)
        if len(commit_list) == 0:
            break

        for commit in commit_list:
            sha = commit["sha"]
            commit_detail = await callGithubAPI_COMMIT_DETAIL(suffix_URL=repo_name, github_id=github_id, sha=sha)
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
