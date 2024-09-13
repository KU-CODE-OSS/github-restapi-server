from fastapi import APIRouter, Response, HTTPException
from settings import *
import httpx
import json
from datetime import datetime
import asyncio

router = APIRouter(
    prefix="/api/repos",
    tags=['/api/repos'],
)

#--- request function ---#
async def request(url, headers):
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)
            return response.json()
        except httpx.TimeoutException:
            return {'error': 408, 'message': 'Request Timeout'}
        except httpx.HTTPStatusError as exc:
            return {'error': exc.response.status_code, 'message': exc.response.text}
        except Exception as e:
            return {'error': 500, 'message': str(e)}
# ------------------------ #

# --- REPOSITORY RELATED URL ---#
async def callGithubAPI(repo_id):
    global remaining_requests, current_token
    
    if remaining_requests <= 0 or current_token is None:
        current_token = await get_new_token()
    
    headers = {
        'Authorization': f'token {current_token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    url = f'{API_URL}/repositories/{repo_id}'
    return await request(url, headers)
# ------------------------ #

async def callGithubAPI_DETAIL(suffix_URL, github_id):
    global remaining_requests, current_token
    
    if remaining_requests <= 0 or current_token is None:
        current_token = await get_new_token()
    
    headers = {
        'Authorization': f'token {current_token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    url = f'{API_URL}/repos/{github_id}/{suffix_URL}'
    return await request(url, headers)
# ------------------------ #

async def callGithubAPI_COMMIT_COUNT(suffix_URL, github_id):
    global remaining_requests, current_token
    
    if remaining_requests <= 0 or current_token is None:
        current_token = await get_new_token()
    
    headers = {
        'Authorization': f'token {current_token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    url = f'{API_URL}/search/commits?q=repo:{github_id}/{suffix_URL}+committer-date:>=2008-02-08T00:00:00Z'
    return await request(url, headers)
# ------------------------ #

async def callGithubAPI_ISSUE_COUNT(suffix_URL, github_id, state):
    global remaining_requests, current_token
    
    if remaining_requests <= 0 or current_token is None:
        current_token = await get_new_token()
    
    headers = {
        'Authorization': f'token {current_token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    url = f'{API_URL}/search/issues?q=repo:{github_id}/{suffix_URL}+type:issue+state:{state}'
    return await request(url, headers)
# ------------------------ #

async def callGithubAPI_PULLS_COUNT(suffix_URL, github_id, state):
    global remaining_requests, current_token
    
    if remaining_requests <= 0 or current_token is None:
        current_token = await get_new_token()
    
    headers = {
        'Authorization': f'token {current_token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    url = f'{API_URL}/search/issues?q=repo:{github_id}/{suffix_URL}+type:pr+state:{state}'
    return await request(url, headers)
# ------------------------ #

# --- CONTRIBUTOR RELATED URL ---#
async def callGithubAPI_CONTRIBUTOR(suffix_URL, github_id, page):
    global remaining_requests, current_token
    
    if remaining_requests <= 0 or current_token is None:
        current_token = await get_new_token()
    
    headers = {
        'Authorization': f'token {current_token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    url = f'{API_URL}/repos/{github_id}/{suffix_URL}/contributors?q=&page={page}&per_page=100'
    return await request(url, headers)
# ------------------------ #

# ---ISSUE RELATED URL ---#
async def callGithubAPI_ISSUE(suffix_URL, github_id, state, page, since):
    global remaining_requests, current_token
    
    if remaining_requests <= 0 or current_token is None:
        current_token = await get_new_token()
    
    headers = {
        'Authorization': f'token {current_token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    url = f'{API_URL}/repos/{github_id}/{suffix_URL}/issues?q=&since={since}&state={state}&page={page}&per_page=100'
    return await request(url, headers)

# --- PR RELATED URL ---#
async def callGithubAPI_PULL(suffix_URL, github_id, state, page, since):
    global remaining_requests, current_token
    
    if remaining_requests <= 0 or current_token is None:
        current_token = await get_new_token()
    
    headers = {
        'Authorization': f'token {current_token}',
        'Accept': 'application/vnd.github.v3+json',
    }
    url= f'{API_URL}/repos/{github_id}/{suffix_URL}/pulls?q=&since={since}&state={state}&page={page}&per_page=100'
    return await request(url, headers)
# ------------------------ #

# --- COMMIT RELATED URL ---#
async def callGithubAPI_COMMIT(suffix_URL, github_id, page, since, per_page):
    global remaining_requests, current_token
    
    if remaining_requests <= 0 or current_token is None:
        current_token = await get_new_token()
    
    headers = {
        'Authorization': f'token {current_token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    url = f'{API_URL}/repos/{github_id}/{suffix_URL}/commits?q=&since={since}&page={page}&per_page={per_page}'
    return await request(url, headers)
# ------------------------ #

async def callGithubAPI_COMMIT_DETAIL(suffix_URL, github_id, sha):
    global remaining_requests, current_token
    
    if remaining_requests <= 0 or current_token is None:
        current_token = await get_new_token()
    
    headers = {
        'Authorization': f'token {current_token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    url = f'{API_URL}/repos/{github_id}/{suffix_URL}/commits/{sha}'
    return await request(url, headers)
# ------------------------ #

# -------------------- Get all Data ------------------------------#
@router.get('', response_class=Response)
async def get_repo_data(github_id: str, repo_id: str):
    repo = await callGithubAPI(repo_id=repo_id)
    if 'error' in repo:
        if repo['error'] == 404:
            raise HTTPException(status_code=404, detail=f"Repository {repo_id} not found")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to fetch repository: {repo['message']}")

    repo_name = repo["name"]

    # Add delay between requests
    await asyncio.sleep(REQ_DELAY)
    commit_counts = await callGithubAPI_COMMIT_COUNT(suffix_URL=repo_name, github_id=github_id)
    commit_count = commit_counts.get("total_count", 0) if 'error' not in commit_counts else 0

    await asyncio.sleep(REQ_DELAY)
    open_issues = await callGithubAPI_ISSUE_COUNT(suffix_URL=repo_name, github_id=github_id, state="open")
    open_issue_count = open_issues.get("total_count", 0) if 'error' not in open_issues else 0

    await asyncio.sleep(REQ_DELAY)
    closed_issues = await callGithubAPI_ISSUE_COUNT(suffix_URL=repo_name, github_id=github_id, state="closed")
    closed_issue_count = closed_issues.get("total_count", 0) if 'error' not in closed_issues else 0

    await asyncio.sleep(REQ_DELAY)
    open_prs = await callGithubAPI_PULLS_COUNT(suffix_URL=repo_name, github_id=github_id, state="open")
    open_pr_count = open_prs.get("total_count", 0) if 'error' not in open_prs else 0

    await asyncio.sleep(REQ_DELAY)
    closed_prs = await callGithubAPI_PULLS_COUNT(suffix_URL=repo_name, github_id=github_id, state="closed")
    closed_pr_count = closed_prs.get("total_count", 0) if 'error' not in closed_prs else 0

    await asyncio.sleep(REQ_DELAY)
    languages = await callGithubAPI_DETAIL(suffix_URL=f'{repo_name}/languages', github_id=github_id)
    language_list = list(languages.keys()) if 'error' not in languages else []

    # Pagination logic for contributors
    contributors_list = []
    page = 1
    total_contributors_count = 0

    while True:
        await asyncio.sleep(REQ_DELAY)
        contributors = await callGithubAPI_CONTRIBUTOR(suffix_URL=repo_name, github_id=github_id, page=page)

        if 'error' in contributors:
            raise HTTPException(status_code=404, detail=f"Contributors in {repo_name} not found")
        
        total_contributors_count += len(contributors)

        for contributor in contributors:
            if 'login' in contributor:
                contributors_list.append(contributor['login'])

        # If fewer than 100 contributors are returned, we've reached the end
        if len(contributors) < 100:
            break

        page += 1

    await asyncio.sleep(REQ_DELAY)
    readme = await callGithubAPI_DETAIL(suffix_URL=f'{repo_name}/readme', github_id=github_id)
    has_readme = True if 'error' not in readme else False

    await asyncio.sleep(REQ_DELAY)
    latest_release = await callGithubAPI_DETAIL(suffix_URL=f'{repo_name}/releases/latest', github_id=github_id)
    release_version = latest_release.get('tag_name', None) if 'error' not in latest_release else None

    repo_item = {
        'id': repo["id"],
        'name': repo["name"],
        'url': repo["html_url"],
        'owner_github_id': repo["owner"]["login"],
        'created_at': repo["created_at"],
        'updated_at': repo["updated_at"],
        'forked': repo['fork'],
        'forks_count': repo["forks_count"],
        'stars_count': repo["stargazers_count"],
        'commit_count': commit_count,
        'open_issue_count': open_issue_count,
        'closed_issue_count': closed_issue_count,
        'open_pr_count': open_pr_count,
        'closed_pr_count': closed_pr_count,
        'language': language_list,
        'contributors': contributors_list,
        'license': repo["license"]["name"] if repo["license"] else None,
        'has_readme': has_readme,
        'description': repo["description"],
        'release_version': release_version,
        'crawled_date': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    }

    return Response(content=json.dumps(repo_item), media_type="application/json")


#--------------------- Get data individually --------------------#
@router.get('/id', response_class=Response)
async def get_repo_id(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    if 'error' in repoinfo:
        raise HTTPException(status_code=repoinfo['error'], detail=repoinfo['message'])

    item = {'id': repoinfo["id"]}
    return Response(content=json.dumps(item), media_type="application/json")

@router.get('/node_id', response_class=Response)
async def get_repo_node_id(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    if 'error' in repoinfo:
        raise HTTPException(status_code=repoinfo['error'], detail=repoinfo['message'])

    item = {'node_id': repoinfo["node_id"]}
    return Response(content=json.dumps(item), media_type="application/json")

@router.get('/name', response_class=Response)
async def get_repo_name(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    if 'error' in repoinfo:
        raise HTTPException(status_code=repoinfo['error'], detail=repoinfo['message'])

    item = {'name': repoinfo["name"]}
    return Response(content=json.dumps(item), media_type="application/json")

@router.get('/full_name', response_class=Response)
async def get_repo_full_name(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    if 'error' in repoinfo:
        raise HTTPException(status_code=repoinfo['error'], detail=repoinfo['message'])

    item = {'full_name': repoinfo["full_name"]}
    return Response(content=json.dumps(item), media_type="application/json")

@router.get('/html_url', response_class=Response)
async def get_repo_html_url(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    if 'error' in repoinfo:
        raise HTTPException(status_code=repoinfo['error'], detail=repoinfo['message'])

    item = {'html_url': repoinfo["html_url"]}
    return Response(content=json.dumps(item), media_type="application/json")

@router.get('/owner', response_class=Response)
async def get_repo_owner(github_id: str, repo_name: str):
    item = {'owner': github_id}
    return Response(content=json.dumps(item), media_type="application/json")

@router.get('/created_at', response_class=Response)
async def get_repo_created_at(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    if 'error' in repoinfo:
        raise HTTPException(status_code=repoinfo['error'], detail=repoinfo['message'])

    item = {'created_at': repoinfo["created_at"]}
    return Response(content=json.dumps(item), media_type="application/json")

@router.get('/updated_at', response_class=Response)
async def get_repo_updated_at(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    if 'error' in repoinfo:
        raise HTTPException(status_code=repoinfo['error'], detail=repoinfo['message'])

    item = {'updated_at': repoinfo["updated_at"]}
    return Response(content=json.dumps(item), media_type="application/json")

@router.get('/pushed_at', response_class=Response)
async def get_repo_pushed_at(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    if 'error' in repoinfo:
        raise HTTPException(status_code=repoinfo['error'], detail=repoinfo['message'])

    item = {'pushed_at': repoinfo["pushed_at"]}
    return Response(content=json.dumps(item), media_type="application/json")

@router.get('/clone', response_class=Response)
async def get_repo_clone(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    if 'error' in repoinfo:
        raise HTTPException(status_code=repoinfo['error'], detail=repoinfo['message'])

    item = {
        'https': repoinfo["clone_url"],
        'ssh': repoinfo["ssh_url"]
    }
    return Response(content=json.dumps(item), media_type="application/json")

@router.get('/stars_count', response_class=Response)
async def get_repo_stars_count(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    if 'error' in repoinfo:
        raise HTTPException(status_code=repoinfo['error'], detail=repoinfo['message'])

    item = {'stars': repoinfo["stargazers_count"]}
    return Response(content=json.dumps(item), media_type="application/json")

@router.get('/commit_count', response_class=Response)
async def get_repo_commit_count(github_id: str, repo_name: str):

    commit_counts = await callGithubAPI_COMMIT_COUNT(suffix_URL=repo_name, github_id=github_id)
    commit_count = commit_counts.get("total_count", 0) if 'error' not in commit_counts else 0

    return Response(content=json.dumps(commit_count), media_type="application/json")

@router.get('/watchers_count', response_class=Response)
async def get_repo_watchers_count(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    if 'error' in repoinfo:
        raise HTTPException(status_code=repoinfo['error'], detail=repoinfo['message'])

    item = {'watchers': repoinfo["watchers"]}
    return Response(content=json.dumps(item), media_type="application/json")

@router.get('/repo_size', response_class=Response)
async def get_repo_size(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    if 'error' in repoinfo:
        raise HTTPException(status_code=repoinfo['error'], detail=repoinfo['message'])

    item = {'size': repoinfo["size"]}
    return Response(content=json.dumps(item), media_type="application/json")

@router.get('/forks_count', response_class=Response)
async def get_repo_forks_count(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    if 'error' in repoinfo:
        raise HTTPException(status_code=repoinfo['error'], detail=repoinfo['message'])

    item = {'forks': repoinfo["forks"]}
    return Response(content=json.dumps(item), media_type="application/json")

@router.get('/open_issues_count', response_class=Response)
async def get_repo_open_issues_count(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    if 'error' in repoinfo:
        raise HTTPException(status_code=repoinfo['error'], detail=repoinfo['message'])

    item = {'open_issues_count': repoinfo["open_issues_count"]}
    return Response(content=json.dumps(item), media_type="application/json")

@router.get('/closed_issues_count', response_class=Response)
async def get_repo_closed_issues_count(github_id: str, repo_name: str):

    closed_issues = await callGithubAPI_ISSUE_COUNT(suffix_URL=repo_name, github_id=github_id, state="closed")
    closed_issue_count = closed_issues.get("total_count", 0) if 'error' not in closed_issues else 0
    
    return Response(content=json.dumps(closed_issue_count), media_type="application/json")

@router.get('/laguages', response_class=Response)
async def get_repo_languages(github_id: str, repo_name: str):
    languages = await callGithubAPI(suffix_URL=f"{repo_name}/languages", github_id=github_id)
    if 'error' in languages:
        raise HTTPException(status_code=languages['error'], detail=languages['message'])

    language_names = list(languages.keys())
    item = {'languages': language_names}
    return Response(content=json.dumps(item, indent=4, default=str), media_type="application/json")

@router.get('/contributors', response_class=Response)
async def get_repo_contributors(github_id: str, repo_name: str):
    contributors = await callGithubAPI(suffix_URL=f"{repo_name}/contributors", github_id=github_id)
    if 'error' in contributors:
        raise HTTPException(status_code=contributors['error'], detail=contributors['message'])

    contributors_names = [contributor['login'] for contributor in contributors if 'login' in contributor]
    item = {'contributor': contributors_names}
    return Response(content=json.dumps(item), media_type="application/json")

@router.get('/license', response_class=Response)
async def get_repo_license(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    if 'error' in repoinfo:
        raise HTTPException(status_code=repoinfo['error'], detail=repoinfo['message'])

    item = {'license': repoinfo["license"]["key"]}
    return Response(content=json.dumps(item), media_type="application/json")

@router.get('/has_readme', response_class=Response)
async def get_repo_has_readme(github_id: str, repo_name: str):
    readme_info = await callGithubAPI(suffix_URL=f"{repo_name}/readme", github_id=github_id)
    has_readme = False if 'error' in readme_info else True

    item = {'has_readme': has_readme}
    return Response(content=json.dumps(item), media_type="application/json")

@router.get('/description', response_class=Response)
async def get_repo_description(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    if 'error' in repoinfo:
        raise HTTPException(status_code=repoinfo['error'], detail=repoinfo['message'])

    item = {'description': repoinfo["description"]}
    return Response(content=json.dumps(item, indent=4, default=str), media_type="application/json")

@router.get('/release_version', response_class=Response)
async def get_repo_release_version(github_id: str, repo_name: str):
    latest_release = await callGithubAPI(suffix_URL=f"{repo_name}/releases/latest", github_id=github_id)
    release_version = latest_release.get('tag_name', 'No release found') if 'error' not in latest_release else 'No release found'

    item = {'release_version': release_version}
    return Response(content=json.dumps(item), media_type="application/json")

@router.get('/fork', response_class=Response)
async def get_repo_fork(github_id: str, repo_name: str):
    repoinfo = await callGithubAPI(suffix_URL=repo_name, github_id=github_id)
    if 'error' in repoinfo:
        raise HTTPException(status_code=repoinfo['error'], detail=repoinfo['message'])

    item = {'fork': repoinfo["fork"]}
    return Response(content=json.dumps(item), media_type="application/json")

@router.get('/fork_users', response_class=Response)
async def get_repo_fork_users(github_id: str, repo_name: str):
    page = 1
    user_list = []
    while True:
        users = await callGithubAPI(suffix_URL=f'{repo_name}/forks?q=page={page}&per_page=100', github_id=github_id)
        if 'error' in users or not users:
            break

        for key in users:
            d = {
                'github_id': key['owner']['login'],
                'id': key['owner']['id'],
                'url': key['owner']['url']
            }
            user = {
                'owner': d,
                'id': key['id'],
                'name': key['name'],
                'full_name': key['full_name'],
                'stars': key['stargazers_count'],
                'watchers': key["watchers"],
                'forks': key["forks"],
                'open_issues_count': key['open_issues_count'],
            }
            user_list.append(user)
        page += 1
    return Response(content=json.dumps(user_list), media_type="application/json")
# ---------------------------------------------------------------#

# -------------------- /repos/contributor ------------------------------#
@router.get('/contributor', response_class=Response)
async def get_repo_contributors(github_id: str, repo_name: str):
    contributors_list = []
    page = 1
    total_contributors_count = 0

    while True:
        await asyncio.sleep(REQ_DELAY)
        contributors = await callGithubAPI_CONTRIBUTOR(suffix_URL=repo_name, github_id=github_id, page=page)

        if 'error' in contributors:
            raise HTTPException(status_code=404, detail=f"Contributors in {repo_name} not found")
        
        total_contributors_count += len(contributors)
        print(f"Page {page}: {len(contributors)} contributor(s)")

        for contributor in contributors:
            if 'login' in contributor and 'contributions' in contributor:
                contributor_data = {
                    'repo_url': f'{HTML_URL}/{github_id}/{repo_name}',
                    'login': contributor["login"],
                    'contributions': contributor["contributions"]
                }
                contributors_list.append(contributor_data)

        # If fewer than 100 contributors are returned, we've reached the end
        if len(contributors) < 100:
            break

        page += 1

    print(f'Total contributors: {total_contributors_count}')
    return Response(content=json.dumps(contributors_list), media_type="application/json")

#----------------------------------------------------------------#

# -------------------- /repos/issues ------------------------------#
@router.get('/issues', response_class=Response)
async def get_repo_issues(github_id: str, repo_name: str, since: str):
    issues = []
    states = ['open', 'closed']

    total_issue_count = 0

    for state in states:
        page = 1
        while True:
            await asyncio.sleep(REQ_DELAY)
            issue_list = await callGithubAPI_ISSUE(suffix_URL=repo_name, github_id=github_id, state=state, page=page, since=since)
            total_issue_count += len(issue_list)
            print(f'State: {state}')
            print(f"Page {page}: {len(issue_list)} issue(s)")
            if 'error' in issue_list or not issue_list:
                break

            for issue in issue_list:
                issue_data = {
                    'id': issue['id'],
                    'owner_github_id': github_id,
                    'repo_url': f'{HTML_URL}/{github_id}/{repo_name}',
                    'state': issue['state'],
                    'title': issue['title'],
                    'publisher_github_id': issue['user']['login'] if issue['user'] else 'Unknown',
                    'last_update': issue['created_at'],
                }
                issues.append(issue_data)
            
            if len(issue_list) < 100:
                break

            page += 1
    print(f'Total issues: {total_issue_count}')
    return Response(content=json.dumps(issues), media_type="application/json")

@router.get('/issues/open', response_class=Response)
async def get_open_issues(github_id: str, repo_name: str, since: str):
    page = 1
    issues = []
    state = "open"
    while True:
        issue_list = await callGithubAPI_ISSUE(suffix_URL=repo_name, github_id=github_id, state=state, page=page, since=since)
        if 'error' in issue_list or not issue_list:
            break

        for issue in issue_list:
            issue_data = {
                'id': issue['id'],
                'owner_github_id': github_id,
                'repo_url': f'{HTML_URL}/{github_id}/{repo_name}',
                'state': issue['state'],
                'title': issue['title'],
                'publisher_github_id': issue['user']['login'],
                'last_update': issue['created_at'],
            }
            issues.append(issue_data)

        if len(issue_list) < 100:
            break
        
        page += 1

    return Response(content=json.dumps(issues), media_type="application/json")

@router.get('/issues/closed', response_class=Response)
async def get_closed_issues(github_id: str, repo_name: str, since: str):
    page = 1
    issues = []
    state = "closed"
    while True:
        issue_list = await callGithubAPI_ISSUE(suffix_URL=repo_name, github_id=github_id, state=state, page=page, since=since)
        if 'error' in issue_list or not issue_list:
            break

        for issue in issue_list:
            issue_data = {
                'id': issue['id'],
                'owner_github_id': github_id,
                'repo_url': f'{HTML_URL}/{github_id}/{repo_name}',
                'state': issue['state'],
                'title': issue['title'],
                'publisher_github_id': issue['user']['login'],
                'last_update': issue['created_at'],
            }
            issues.append(issue_data)

        if len(issue_list) < 100:
            break

        page += 1

    return Response(content=json.dumps(issues), media_type="application/json")
#----------------------------------------------------------------#

#-------------------- repos/pulls ------------------------------#
@router.get('/pulls', response_class=Response)
async def get_repo_pulls(github_id: str, repo_name: str, since: str):
    pulls = []
    states = ['open', 'closed']

    total_pull_count = 0

    for state in states:
        page = 1
        while True:
            await asyncio.sleep(REQ_DELAY)
            pull_list = await callGithubAPI_PULL(suffix_URL=repo_name, github_id=github_id, state=state, page=page, since=since)
            total_pull_count += len(pull_list)
            print(f'State: {state}')
            print(f"Page {page}: {len(pull_list)} PR(s)")
            if 'error' in pull_list or not pull_list:
                break

            for pull in pull_list:
                pull_data = {
                    'id': pull["id"],
                    'owner_github_id': github_id,
                    'state': pull["state"],
                    'title': pull["title"],
                    'repo_url': f'{HTML_URL}/{github_id}/{repo_name}',
                    'requester_id': pull['user']['login'],
                    'published_date': pull['created_at'],
                    'last_update': pull['updated_at'],
                }
                pulls.append(pull_data)

            if len(pull_list) < 100:
                break

            page += 1
    print(f'Total pulls: {total_pull_count}')

    return Response(content=json.dumps(pulls), media_type="application/json")

@router.get('/pulls/open', response_class=Response)
async def get_open_pulls(github_id: str, repo_name: str, since: str):
    page = 1
    pulls = []
    state = "open"
    while True:
        await asyncio.sleep(REQ_DELAY)
        pulls_list = await callGithubAPI_PULL(suffix_URL=repo_name, github_id=github_id, state=state, page=page, since=since)
        if 'error' in pulls_list or not pulls_list:
            break

        for pull in pulls_list:
            pull_data = {
                'id': pull["id"],
                'owner_github_id': github_id,
                'state': pull["state"],
                'title': pull["title"],
                'repo_url': f'{HTML_URL}/{github_id}/{repo_name}',
                'requester_id': pull['user']['login'],
                'last_update': pull['created_at'],
            }
            pulls.append(pull_data)

        if len(pulls_list) < 100:
            break
        
        page += 1

    return Response(content=json.dumps(pulls), media_type="application/json")

#-------------------- repos/commits ------------------------------#
@router.get('/commit', response_class=Response)
async def get_commits(github_id: str, repo_name: str, since: str):
    page = 1
    commits = []
    per_page = 100  
    max_pages = 20
    total_commit_count = 0

    try:
        while page <= max_pages:
            commit_list = await callGithubAPI_COMMIT(suffix_URL=repo_name, github_id=github_id, page=page, since=since, per_page=per_page)
            if 'error' in commit_list or not commit_list:
                break

            total_commit_count += len(commit_list)
            print(f"Page {page}: {len(commit_list)} commit(s)")

            for commit in commit_list:
                sha = commit["sha"]
                await asyncio.sleep(REQ_DELAY)
                commit_detail = await callGithubAPI_COMMIT_DETAIL(suffix_URL=repo_name, github_id=github_id, sha=commit["sha"])
                if 'stats' not in commit_detail or 'commit' not in commit_detail or 'author' not in commit_detail['commit']:
                    commit_detail = {
                        'stats': {'additions': 0, 'deletions': 0},
                        'commit': {'author': {'date': 'Unknown'}}
                    }

                commit_data = {
                    'sha': sha,
                    'repo_url': f'{HTML_URL}/{github_id}/{repo_name}',
                    'owner_github_id': github_id,
                    'committer_github_id': commit['author']['login'] if commit['author'] else 'Unknown',
                    'added_lines': commit_detail['stats'].get('additions', 0),
                    'deleted_lines': commit_detail['stats'].get('deletions', 0),
                    'last_update': commit_detail['commit']['author'].get('date', 'Unknown'),
                }
                commits.append(commit_data)

            if len(commit_list) < per_page:
                break

            page += 1

        print(f'Total commits: {total_commit_count}')
        return Response(content=json.dumps(commits), media_type="application/json")

    except Exception as e:
        print(f"Error: {e}")
        if commits:
            return Response(content=json.dumps(commits), media_type="application/json")
        else:
            raise HTTPException(status_code=500, detail="Failed to fetch commits due to token exhaustion or other error.")
