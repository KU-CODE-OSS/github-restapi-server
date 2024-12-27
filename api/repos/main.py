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

# GraphQL API 호출 함수 수정
async def callGithubAPI_GRAPHQL(query: str):
    url = "https://api.github.com/graphql"
    headers = {
        'Authorization': f'token {current_token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={"query": query}, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.json().get("message", "Error occurred")}


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

async def callGithubAPI_contributed_COMMIT_COUNT(suffix_URL, parent_github_id, github_id):
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

async def callGithubAPI_contributed_ISSUE_COUNT(suffix_URL, parent_github_id, github_id, state):
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

async def callGithubAPI_contributed_PULLS_COUNT(suffix_URL, parent_github_id, github_id, state):
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
    repo = await callGithubAPIRepo(repo_id=repo_id)
    if 'error' in repo:
        if repo['error'] == 404:
            raise HTTPException(status_code=404, detail=f"Repository {repo_id} not found")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to fetch repository: {repo.get('message', 'Unknown error')}")

    if repo.get("fork", False) == True:
        parent_github_id = repo.get("parent", {}).get("owner", {}).get("login", github_id)
        repo_name = repo.get("parent", {}).get("name", "")
    else:
        parent_github_id = github_id
        repo_name = repo.get("name", "")

    # Repository owner details
    await asyncio.sleep(REQ_DELAY)
    contributed_commit_counts = await callGithubAPI_contributed_COMMIT_COUNT(suffix_URL=repo_name, parent_github_id=parent_github_id, github_id=github_id)
    contributed_commit_count = contributed_commit_counts.get("total_count", 0) if 'error' not in contributed_commit_counts else 0

    await asyncio.sleep(REQ_DELAY)
    contributed_open_issues = await callGithubAPI_contributed_ISSUE_COUNT(suffix_URL=repo_name, parent_github_id=parent_github_id, github_id=github_id, state="open")
    contributed_open_issue_count = contributed_open_issues.get("total_count", 0) if 'error' not in contributed_open_issues else 0

    await asyncio.sleep(REQ_DELAY)
    contributed_closed_issues = await callGithubAPI_contributed_ISSUE_COUNT(suffix_URL=repo_name, parent_github_id=parent_github_id, github_id=github_id, state="closed")
    contributed_closed_issue_count = contributed_closed_issues.get("total_count", 0) if 'error' not in contributed_closed_issues else 0

    await asyncio.sleep(REQ_DELAY)
    contributed_open_prs = await callGithubAPI_contributed_PULLS_COUNT(suffix_URL=repo_name, parent_github_id=parent_github_id, github_id=github_id, state="open")
    contributed_open_pr_count = contributed_open_prs.get("total_count", 0) if 'error' not in contributed_open_prs else 0

    await asyncio.sleep(REQ_DELAY)
    contributed_closed_prs = await callGithubAPI_contributed_PULLS_COUNT(suffix_URL=repo_name, parent_github_id=parent_github_id, github_id=github_id, state="closed")
    contributed_closed_pr_count = contributed_closed_prs.get("total_count", 0) if 'error' not in contributed_closed_prs else 0

    # Repository overall
    graphql_query = """
    {
      repository(owner: "%s", name: "%s") {
        defaultBranchRef {
          target {
            ... on Commit {
              history {
                totalCount
              }
            }
          }
        }
      }
    }
    """ % (parent_github_id, repo_name)

    await asyncio.sleep(REQ_DELAY)
    try:
        commit_count_response = await callGithubAPI_GRAPHQL(query=graphql_query)
        commit_count = (
            commit_count_response.get("data", {})
            .get("repository", {})
            .get("defaultBranchRef", {})
            .get("target", {})
            .get("history", {})
            .get("totalCount", 0)
            if commit_count_response is not None else 0
        )
    except AttributeError:
        commit_count = 0
    except:
        commit_count = 0

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
        try:
            await asyncio.sleep(REQ_DELAY)
            contributors = await callGithubAPI_CONTRIBUTOR(suffix_URL=repo_name, github_id=github_id, page=page)

            if 'error' in contributors:
                raise HTTPException(status_code=404, detail=f"Contributors in {repo_name} not found")

            total_contributors_count += len(contributors)

            for contributor in contributors:
                if 'login' in contributor:
                    contributors_list.append(contributor.get('login', None))

            # If fewer than 100 contributors are returned, we've reached the end
            if len(contributors) < 100:
                break

            page += 1
        except:
            break

    await asyncio.sleep(REQ_DELAY)
    readme = await callGithubAPI_DETAIL(suffix_URL=f'{repo_name}/readme', github_id=github_id)
    has_readme = True if 'error' not in readme else False

    await asyncio.sleep(REQ_DELAY)
    latest_release = await callGithubAPI_DETAIL(suffix_URL=f'{repo_name}/releases/latest', github_id=github_id)
    release_version = latest_release.get('tag_name', None) if 'error' not in latest_release else None

    # Handle the license information
    license_info = repo.get("license")
    license_name = license_info.get("name") if license_info else None

    repo_item = {
        'id': repo.get("id"),
        'name': repo.get("name"),
        'url': repo.get("html_url"),
        'owner_github_id': repo.get("owner", {}).get("login"),
        'created_at': repo.get("created_at"),
        'updated_at': repo.get("updated_at"),
        'forked': repo.get('fork', False),
        'forks_count': repo.get("forks_count"),
        'stars_count': repo.get("stargazers_count"),
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
        'license': license_name,
        'has_readme': has_readme,
        'description': repo.get("description"),
        'release_version': release_version,
        'crawled_date': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    }

    print("-" * 10)
    print("api/repos")
    print(repo_item)
    return Response(content=json.dumps(repo_item), media_type="application/json")
# ------------------------ #

# -------------------- /repos/contributor ------------------------------#
@router.get('/contributor', response_class=Response)
async def get_repo_contributors(github_id: str, repo_name: str):
    contributors_list = []
    page = 1
    total_contributors_count = 0

    while True:
        await asyncio.sleep(REQ_DELAY)
        contributors = await callGithubAPI_CONTRIBUTOR(suffix_URL=repo_name, github_id=github_id, page=page)

        # If the response contains an error, raise an HTTPException
        if 'error' in contributors:
            raise HTTPException(status_code=404, detail=f"Contributors in {repo_name} not found")
        
        total_contributors_count += len(contributors)
        print(f"Page {page}: {len(contributors)} contributor(s)")

        for contributor in contributors:
            # Using `.get()` to handle possible missing keys or `None` values
            contributor_data = {
                'repo_url': f'{HTML_URL}://{github_id}/{repo_name}',
                'login': contributor.get("login"),
                'contributions': contributor.get("contributions")
            }
            contributors_list.append(contributor_data)

        # If fewer than 100 contributors are returned, we've reached the end
        if len(contributors) < 100:
            break

        page += 1

    print("-" * 20)
    print("api/repos/contributor")
    print(f'{repo_name} - Total contributors: {total_contributors_count}')
    return Response(content=json.dumps(contributors_list), media_type="application/json")
# ------------------------ #

# -------------------- /repos/issues ------------------------------#
@router.get('/issues', response_class=Response)
async def get_repo_issues(github_id: str, repo_name: str, since: str):
    issues = []
    states = ['open', 'closed']
    total_issue_count = 0
    max_issue_count = 500  # Set maximum limit for issues

    for state in states:
        page = 1
        while total_issue_count < max_issue_count:
            await asyncio.sleep(REQ_DELAY)
            issue_list = await callGithubAPI_ISSUE(suffix_URL=repo_name, github_id=github_id, state=state, page=page, since=since)
            
            # Handle potential errors or empty lists
            if 'error' in issue_list or not issue_list:
                break
            
            total_issue_count += len(issue_list)
            print(f'State: {state}')
            print(f"Page {page}: {len(issue_list)} issue(s)")

            for issue in issue_list:
                issue_data = {
                    'id': issue.get('id'),
                    'contributed_github_id': github_id,
                    'repo_url': f'{HTML_URL}://{github_id}/{repo_name}',
                    'state': issue.get('state'),
                    'title': issue.get('title'),
                    'publisher_github_id': issue.get('user', {}).get('login', 'Unknown'),
                    'last_update': issue.get('created_at')
                }
                issues.append(issue_data)

            # Check if the total_issue_count has reached the maximum limit
            if total_issue_count >= max_issue_count or len(issue_list) < 100:
                break

            page += 1

    print("-" * 20)
    print("api/repos/issue")
    print(f'{repo_name} - Total issues: {total_issue_count} since {since}')
    return Response(content=json.dumps(issues), media_type="application/json")
# ------------------------ #

#-------------------- repos/pulls ------------------------------#
@router.get('/pulls', response_class=Response)
async def get_repo_pulls(github_id: str, repo_name: str, since: str):
    pulls = []
    states = ['open', 'closed']
    total_pull_count = 0
    max_pull_count = 500  # Set maximum limit for pulls

    for state in states:
        page = 1
        while total_pull_count < max_pull_count:
            await asyncio.sleep(REQ_DELAY)
            pull_list = await callGithubAPI_PULL(suffix_URL=repo_name, github_id=github_id, state=state, page=page, since=since)

            # Handle potential errors or empty lists
            if 'error' in pull_list or not pull_list:
                break
            
            total_pull_count += len(pull_list)
            print(f'State: {state}')
            print(f"Page {page}: {len(pull_list)} PR(s)")

            for pull in pull_list:
                pull_data = {
                    'id': pull.get("id"),
                    'contributed_github_id': github_id,
                    'state': pull.get("state"),
                    'title': pull.get("title"),
                    'repo_url': f'{HTML_URL}/{github_id}/{repo_name}',
                    'requester_id': pull.get('user', {}).get('login', 'Unknown'),
                    'published_date': pull.get('created_at'),
                    'last_update': pull.get('updated_at'),
                }
                pulls.append(pull_data)

            # Check if the total_pull_count has reached the maximum limit
            if total_pull_count >= max_pull_count or len(pull_list) < 100:
                break

            page += 1

    print("-" * 20)
    print("api/repos/pr")
    print(f'{repo_name} - Total pulls: {total_pull_count} since {since}')

    return Response(content=json.dumps(pulls), media_type="application/json")

# ------------------------ #

#-------------------- repos/commits ------------------------------#
@router.get('/commit', response_class=Response)
async def get_commits(github_id: str, repo_name: str, since: str):
    page = 1
    commits = []
    per_page = 100  
    max_pages = 2
    total_commit_count = 0

    try:
        while page <= max_pages:
            commit_list = await callGithubAPI_COMMIT(suffix_URL=repo_name, github_id=github_id, page=page, since=since, per_page=per_page)
            if 'error' in commit_list or not commit_list:
                break

            total_commit_count += len(commit_list)
            print("-"*20)
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
                    'contributed_github_id': github_id,
                    'author_github_id': commit['author']['login'] if commit['author'] else 'Unknown',
                    'added_lines': commit_detail['stats'].get('additions', 0),
                    'deleted_lines': commit_detail['stats'].get('deletions', 0),
                    'last_update': commit_detail['commit']['author'].get('date', 'Unknown'),
                }
                commits.append(commit_data)

            if len(commit_list) < per_page:
                break

            page += 1

        print("-"*20)
        print("api/repos/commit")
        print(f'{repo_name} - Total commits: {total_commit_count} since {since}')
        return Response(content=json.dumps(commits), media_type="application/json")

    except Exception as e:
        print(f"Error: {e}")
        if commits:
            return Response(content=json.dumps(commits), media_type="application/json")
        else:
            raise HTTPException(status_code=500, detail="Failed to fetch commits due to token exhaustion or other error.")
#----------------------------------------------------------------#