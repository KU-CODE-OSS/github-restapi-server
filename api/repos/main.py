from fastapi import APIRouter, Response, HTTPException

from utils.settings import *
from commons.api_client import request

import httpx
import json
from datetime import datetime
import asyncio

router = APIRouter(
    prefix="/api/repos",
    tags=['/api/repos'],
)

# --- REPOSITORY RELATED URL ---#
async def callGithubAPIRepo(repo_id):
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

async def callGithubAPI_OWNER_COMMIT_COUNT(suffix_URL, parent_github_id, github_id):
    global remaining_requests, current_token
    
    if remaining_requests <= 0 or current_token is None:
        current_token = await get_new_token()
    
    headers = {
        'Authorization': f'token {current_token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    url = f'{API_URL}/search/commits?q=repo:{parent_github_id}/{suffix_URL}+committer-date:>=2008-02-08T00:00:00Z+author:{github_id}'
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

async def callGithubAPI_OWNER_ISSUE_COUNT(suffix_URL, parent_github_id, github_id, state):
    global remaining_requests, current_token
    
    if remaining_requests <= 0 or current_token is None:
        current_token = await get_new_token()
    
    headers = {
        'Authorization': f'token {current_token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    url = f'{API_URL}/search/issues?q=repo:{parent_github_id}/{suffix_URL}+type:issue+state:{state}+author:{github_id}'
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

async def callGithubAPI_OWNER_PULLS_COUNT(suffix_URL, parent_github_id, github_id, state):
    global remaining_requests, current_token
    
    if remaining_requests <= 0 or current_token is None:
        current_token = await get_new_token()
    
    headers = {
        'Authorization': f'token {current_token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    url = f'{API_URL}/search/issues?q=repo:{parent_github_id}/{suffix_URL}+type:pr+state:{state}+author:{github_id}'
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
    # Fetch repository information

    await asyncio.sleep(REQ_DELAY)
    repo = await callGithubAPIRepo(repo_id=repo_id)
    if 'error' in repo:
        error_message = f"Repository {repo_id} not found" if repo['error'] == 404 else f"Failed to fetch repository: {repo['message']}"
        raise HTTPException(status_code=repo['error'], detail=error_message)

    # Determine if the repository is forked and get parent details if so
    is_fork = repo["fork"]
    parent_github_id = repo["parent"]["owner"]["login"] if is_fork else github_id
    repo_name = repo["name"]
    parent_repo_name = repo["parent"]["name"] if is_fork else repo_name

    # Fetch contributed commit counts, issues, and PRs for the owner
    await asyncio.sleep(REQ_DELAY)
    contributed_commit_counts = await callGithubAPI_OWNER_COMMIT_COUNT(suffix_URL=parent_repo_name, parent_github_id=parent_github_id, github_id=github_id)
    contributed_commit_count = contributed_commit_counts.get("total_count", 0) if 'error' not in contributed_commit_counts else 0

    await asyncio.sleep(REQ_DELAY)
    contributed_open_issues = await callGithubAPI_OWNER_ISSUE_COUNT(suffix_URL=parent_repo_name, parent_github_id=parent_github_id, github_id=github_id, state="open")
    contributed_open_issue_count = contributed_open_issues.get("total_count", 0) if 'error' not in contributed_open_issues else 0

    await asyncio.sleep(REQ_DELAY)
    contributed_closed_issues = await callGithubAPI_OWNER_ISSUE_COUNT(suffix_URL=parent_repo_name, parent_github_id=parent_github_id, github_id=github_id, state="closed")
    contributed_closed_issue_count = contributed_closed_issues.get("total_count", 0) if 'error' not in contributed_closed_issues else 0

    await asyncio.sleep(REQ_DELAY)
    contributed_open_prs = await callGithubAPI_OWNER_PULLS_COUNT(suffix_URL=parent_repo_name, parent_github_id=parent_github_id, github_id=github_id, state="open")
    contributed_open_pr_count = contributed_open_prs.get("total_count", 0) if 'error' not in contributed_open_prs else 0

    await asyncio.sleep(REQ_DELAY)
    contributed_closed_prs = await callGithubAPI_OWNER_PULLS_COUNT(suffix_URL=parent_repo_name, parent_github_id=parent_github_id, github_id=github_id, state="closed")
    contributed_closed_pr_count = contributed_closed_prs.get("total_count", 0) if 'error' not in contributed_closed_prs else 0

    # Count total commits in forked or non-forked repo
    if is_fork:
        page = 1
        per_page = 100
        since = "2008-02-08T00:00:00Z"
        total_commit_count = 0

        while True:
            await asyncio.sleep(REQ_DELAY)
            commit_list = await callGithubAPI_COMMIT(suffix_URL=repo_name, github_id=github_id, page=page, since=since, per_page=per_page)
            if 'error' in commit_list or not commit_list:
                break
            total_commit_count += len(commit_list)
            if len(commit_list) < per_page:
                break
            page += 1

        commit_count = total_commit_count
    else:
        commit_counts = await callGithubAPI_COMMIT_COUNT(suffix_URL=repo_name, github_id=github_id)
        commit_count = commit_counts.get("total_count", 0) if 'error' not in commit_counts else 0

    # Fetch open and closed issues, and PR counts
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

    # Fetch repository languages
    await asyncio.sleep(REQ_DELAY)
    languages = await callGithubAPI_DETAIL(suffix_URL=f'{repo_name}/languages', github_id=github_id)
    language_list = list(languages.keys()) if 'error' not in languages else []

    # Fetch contributors with pagination
    contributors_list = []
    page = 1
    per_page = 100
    while True:
        await asyncio.sleep(REQ_DELAY)
        contributors = await callGithubAPI_CONTRIBUTOR(suffix_URL=repo_name, github_id=github_id, page=page)
        if 'error' in contributors:
            break
        contributors_list.extend(contributor['login'] for contributor in contributors if 'login' in contributor)
        if len(contributors) < per_page:
            break
        page += 1

    # Check if README exists
    await asyncio.sleep(REQ_DELAY)
    readme = await callGithubAPI_DETAIL(suffix_URL=f'{repo_name}/readme', github_id=github_id)
    has_readme = 'error' not in readme

    # Fetch latest release version
    await asyncio.sleep(REQ_DELAY)
    latest_release = await callGithubAPI_DETAIL(suffix_URL=f'{repo_name}/releases/latest', github_id=github_id)
    release_version = latest_release.get('tag_name', None) if 'error' not in latest_release else None

    # Compile all repository details into the final response
    repo_item = {
        'id': repo["id"],
        'name': repo["name"],
        'url': repo["html_url"],
        'owner_github_id': repo["owner"]["login"],
        'created_at': repo["created_at"],
        'updated_at': repo["updated_at"],
        'forked': is_fork,
        'forks_count': repo["forks_count"],
        'stars_count': repo["stargazers_count"],
        'commit_count': commit_count,
        'open_issue_count': open_issue_count,
        'closed_issue_count': closed_issue_count,
        'open_pr_count': open_pr_count,
        'closed_pr_count': closed_pr_count,
        'contributed_commit_count': contributed_commit_count,
        'contributed_open_issue_count': contributed_open_issue_count,
        'contributed_closed_issue_count': contributed_closed_issue_count,
        'contributed_open_pr_count': contributed_open_pr_count,
        'contributed_closed_pr_count': contributed_closed_pr_count,
        'language': language_list,
        'contributors': contributors_list,
        'license': repo["license"]["name"] if repo["license"] else None,
        'has_readme': has_readme,
        'description': repo["description"],
        'release_version': release_version,
        'crawled_date': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    }

    print(repo_item)
    return Response(content=json.dumps(repo_item), media_type="application/json")

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

#-------------------- repos/commits ------------------------------#
@router.get('/commit', response_class=Response)
async def get_commits(github_id: str, repo_name: str, since: str):
    page = 1
    commits = []
    per_page = 100  
    max_pages = 5
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
                    'author_github_id': commit['author']['login'] if commit['author'] else 'Unknown',
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
#----------------------------------------------------------------#