from fastapi import APIRouter, Response, HTTPException
from utils.settings import *
from commons.api_client import request

import httpx
import json
from datetime import datetime
import asyncio
import base64
import os

router = APIRouter(
    prefix="/api/repos",
    tags=['/api/repos'],
)

# GraphQL API 호출 함수 수정
async def call_github_api_graphql(query: str):
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
async def call_github_api_repo(repo_id):
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

async def call_github_api_detail(suffix_url, github_id):
    global remaining_requests, current_token
    
    if remaining_requests <= 0 or current_token is None:
        current_token = await get_new_token()
    
    headers = {
        'Authorization': f'token {current_token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    url = f'{API_URL}/repos/{github_id}/{suffix_url}'
    return await request(url, headers)
# ------------------------ #

async def call_github_api_commit_count(suffix_url, github_id):
    global remaining_requests, current_token
    
    if remaining_requests <= 0 or current_token is None:
        current_token = await get_new_token()
    
    headers = {
        'Authorization': f'token {current_token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    url = f'{API_URL}/search/commits?q=repo:{github_id}/{suffix_url}+committer-date:>=2008-02-08T00:00:00Z'
    return await request(url, headers)
# ------------------------ #

async def call_github_api_contributed_commit_count(suffix_url, parent_github_id, github_id):
    global remaining_requests, current_token
    
    if remaining_requests <= 0 or current_token is None:
        current_token = await get_new_token()
    
    headers = {
        'Authorization': f'token {current_token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    url = f'{API_URL}/search/commits?q=repo:{parent_github_id}/{suffix_url}+committer-date:>=2008-02-08T00:00:00Z+author:{github_id}'
    return await request(url, headers)
# ------------------------ #

async def call_github_api_issue_count(suffix_url, github_id, state):
    global remaining_requests, current_token
    
    if remaining_requests <= 0 or current_token is None:
        current_token = await get_new_token()
    
    headers = {
        'Authorization': f'token {current_token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    url = f'{API_URL}/search/issues?q=repo:{github_id}/{suffix_url}+type:issue+state:{state}'
    return await request(url, headers)
# ------------------------ #

async def call_github_api_contributed_issue_count(suffix_url, parent_github_id, github_id, state):
    global remaining_requests, current_token
    
    if remaining_requests <= 0 or current_token is None:
        current_token = await get_new_token()
    
    headers = {
        'Authorization': f'token {current_token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    url = f'{API_URL}/search/issues?q=repo:{parent_github_id}/{suffix_url}+type:issue+state:{state}+author:{github_id}'
    return await request(url, headers)
# ------------------------ #

async def call_github_api_pulls_count(suffix_url, github_id, state):
    global remaining_requests, current_token
    
    if remaining_requests <= 0 or current_token is None:
        current_token = await get_new_token()
    
    headers = {
        'Authorization': f'token {current_token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    url = f'{API_URL}/search/issues?q=repo:{github_id}/{suffix_url}+type:pr+state:{state}'
    return await request(url, headers)
# ------------------------ #

async def call_github_api_contributed_pulls_count(suffix_url, parent_github_id, github_id, state):
    global remaining_requests, current_token
    
    if remaining_requests <= 0 or current_token is None:
        current_token = await get_new_token()
    
    headers = {
        'Authorization': f'token {current_token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    url = f'{API_URL}/search/issues?q=repo:{parent_github_id}/{suffix_url}+type:pr+state:{state}+author:{github_id}'
    return await request(url, headers)
# ------------------------ #

# --- CONTRIBUTOR RELATED URL ---#
async def call_github_api_contributor(suffix_url, github_id, page):
    global remaining_requests, current_token
    
    if remaining_requests <= 0 or current_token is None:
        current_token = await get_new_token()
    
    headers = {
        'Authorization': f'token {current_token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    url = f'{API_URL}/repos/{github_id}/{suffix_url}/contributors?q=&page={page}&per_page=100'
    return await request(url, headers)
# ------------------------ #

# ---ISSUE RELATED URL ---#
async def call_github_api_issue(suffix_url, github_id, state, page, since, per_page=100, sort='updated', direction='desc'):
    global remaining_requests, current_token
    
    if remaining_requests <= 0 or current_token is None:
        current_token = await get_new_token()
    
    headers = {
        'Authorization': f'token {current_token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    url = f'{API_URL}/repos/{github_id}/{suffix_url}/issues?q=&since={since}&state={state}&sort={sort}&direction={direction}&page={page}&per_page={per_page}'
    return await request(url, headers)

# --- PR RELATED URL ---#
async def call_github_api_pull(suffix_url, github_id, state, page, since):
    global remaining_requests, current_token
    
    if remaining_requests <= 0 or current_token is None:
        current_token = await get_new_token()
    
    headers = {
        'Authorization': f'token {current_token}',
        'Accept': 'application/vnd.github.v3+json',
    }
    url = f'{API_URL}/repos/{github_id}/{suffix_url}/pulls?q=&since={since}&state={state}&page={page}&per_page=100'
    return await request(url, headers)
# ------------------------ #

# --- COMMIT RELATED URL ---#
async def call_github_api_commit(suffix_url, github_id, page, since, per_page):
    global remaining_requests, current_token
    
    if remaining_requests <= 0 or current_token is None:
        current_token = await get_new_token()
    
    headers = {
        'Authorization': f'token {current_token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    url = f'{API_URL}/repos/{github_id}/{suffix_url}/commits?q=&since={since}&page={page}&per_page={per_page}'
    return await request(url, headers)
# ------------------------ #

async def call_github_api_commit_detail(suffix_url, github_id, sha):
    global remaining_requests, current_token
    
    if remaining_requests <= 0 or current_token is None:
        current_token = await get_new_token()
    
    headers = {
        'Authorization': f'token {current_token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    url = f'{API_URL}/repos/{github_id}/{suffix_url}/commits/{sha}'
    return await request(url, headers)
# ------------------------ #

def calculate_language_percentage(language_bytes):
    total_bytes = sum(language_bytes.values()) if isinstance(language_bytes, dict) else 0
    if total_bytes <= 0:
        return {}
    return {
        language: round((byte_count / total_bytes) * 100, 1)
        for language, byte_count in language_bytes.items()
        if round((byte_count / total_bytes) * 100, 1) > 0.0
    }


def extract_login(value):
    return value.get('login') if isinstance(value, dict) else None


def classify_file_change(file_payload, committed_at):
    path = file_payload.get('filename') or ''
    filename = os.path.basename(path)
    _, extension = os.path.splitext(filename)
    lower_path = path.lower()
    lower_filename = filename.lower()
    dependency_manifests = {
        'package.json',
        'package-lock.json',
        'yarn.lock',
        'pnpm-lock.yaml',
        'requirements.txt',
        'pyproject.toml',
        'poetry.lock',
        'pipfile',
        'pipfile.lock',
        'pom.xml',
        'build.gradle',
        'build.gradle.kts',
        'go.mod',
        'go.sum',
        'cargo.toml',
        'cargo.lock',
        'gemfile',
        'gemfile.lock',
        'composer.json',
        'composer.lock',
    }

    return {
        'path': path,
        'filename': filename,
        'extension': extension[1:].lower() if extension else None,
        'status': file_payload.get('status'),
        'additions': file_payload.get('additions', 0),
        'deletions': file_payload.get('deletions', 0),
        'changes': file_payload.get('changes', 0),
        'committed_at': committed_at,
        'is_workflow_yaml': lower_path.startswith('.github/workflows/') and lower_path.endswith(('.yml', '.yaml')),
        'is_test_file': (
            '/test/' in lower_path
            or '/tests/' in lower_path
            or lower_filename.startswith('test_')
            or lower_filename.endswith('_test.py')
            or lower_filename.endswith('.test.js')
            or lower_filename.endswith('.spec.js')
            or lower_filename.endswith('.test.ts')
            or lower_filename.endswith('.spec.ts')
            or lower_filename.endswith('.test.jsx')
            or lower_filename.endswith('.spec.jsx')
            or lower_filename.endswith('.test.tsx')
            or lower_filename.endswith('.spec.tsx')
        ),
        'is_readme': lower_filename.startswith('readme'),
        'is_dependency_manifest': lower_filename in dependency_manifests,
    }


def decode_github_content(content_payload):
    content = content_payload.get('content') if isinstance(content_payload, dict) else None
    if not content:
        return ''
    try:
        return base64.b64decode(content.replace('\n', '')).decode('utf-8', errors='ignore')
    except Exception:
        return ''


def dependency_evidence_from_readme(readme_text):
    lower_text = readme_text.lower()
    terms = [
        'npm install',
        'pip install',
        'requirements.txt',
        'package.json',
        'yarn add',
        'pnpm install',
        'poetry install',
        'pipenv install',
        'maven',
        'gradle',
        'go mod',
        'cargo build',
        'docker compose',
        'docker-compose',
    ]
    matched_terms = [term for term in terms if term in lower_text]
    return {
        'matched_terms': matched_terms,
        'match_count': len(matched_terms),
    }

# -------------------- Get all Data ------------------------------#
@router.get('', response_class=Response)
async def get_repo_data(github_id: str, repo_id: str):
    repository_data = await call_github_api_repo(repo_id=repo_id)
    if 'error' in repository_data:
        if repository_data['error'] == 404:
            raise HTTPException(status_code=404, detail=f"Repository {repo_id} not found")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to fetch repository: {repository_data.get('message', 'Unknown error')}")

    parent_github_id = github_id
    repository_name = repository_data.get("name", "")

    # Repository owner details
    await asyncio.sleep(REQ_DELAY)
    contributed_commit_counts = await call_github_api_contributed_commit_count(suffix_url=repository_name, parent_github_id=parent_github_id, github_id=github_id)
    contributed_commit_count = contributed_commit_counts.get("total_count", 0) if 'error' not in contributed_commit_counts else 0

    await asyncio.sleep(REQ_DELAY)
    contributed_open_issues = await call_github_api_contributed_issue_count(suffix_url=repository_name, parent_github_id=parent_github_id, github_id=github_id, state="open")
    contributed_open_issue_count = contributed_open_issues.get("total_count", 0) if 'error' not in contributed_open_issues else 0

    await asyncio.sleep(REQ_DELAY)
    contributed_closed_issues = await call_github_api_contributed_issue_count(suffix_url=repository_name, parent_github_id=parent_github_id, github_id=github_id, state="closed")
    contributed_closed_issue_count = contributed_closed_issues.get("total_count", 0) if 'error' not in contributed_closed_issues else 0

    await asyncio.sleep(REQ_DELAY)
    contributed_open_prs = await call_github_api_contributed_pulls_count(suffix_url=repository_name, parent_github_id=parent_github_id, github_id=github_id, state="open")
    contributed_open_pr_count = contributed_open_prs.get("total_count", 0) if 'error' not in contributed_open_prs else 0

    await asyncio.sleep(REQ_DELAY)
    contributed_closed_prs = await call_github_api_contributed_pulls_count(suffix_url=repository_name, parent_github_id=parent_github_id, github_id=github_id, state="closed")
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
    """ % (parent_github_id, repository_name)

    await asyncio.sleep(REQ_DELAY)
    try:
        commit_count_response = await call_github_api_graphql(query=graphql_query)
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
    open_issues = await call_github_api_issue_count(suffix_url=repository_name, github_id=github_id, state="open")
    open_issue_count = open_issues.get("total_count", 0) if 'error' not in open_issues else 0

    await asyncio.sleep(REQ_DELAY)
    closed_issues = await call_github_api_issue_count(suffix_url=repository_name, github_id=github_id, state="closed")
    closed_issue_count = closed_issues.get("total_count", 0) if 'error' not in closed_issues else 0

    await asyncio.sleep(REQ_DELAY)
    open_prs = await call_github_api_pulls_count(suffix_url=repository_name, github_id=github_id, state="open")
    open_pr_count = open_prs.get("total_count", 0) if 'error' not in open_prs else 0

    await asyncio.sleep(REQ_DELAY)
    closed_prs = await call_github_api_pulls_count(suffix_url=repository_name, github_id=github_id, state="closed")
    closed_pr_count = closed_prs.get("total_count", 0) if 'error' not in closed_prs else 0

    await asyncio.sleep(REQ_DELAY)
    languages = await call_github_api_detail(suffix_url=f'{repository_name}/languages', github_id=github_id)
    language_list = list(languages.keys()) if 'error' not in languages else []
    # Dictionary consists of Languages & Bytes of each language
    language_bytes = languages if 'error' not in languages else {}

    # Pagination logic for contributors
    contributors_list = []
    page = 1
    total_contributors_count = 0

    while True:
        try:
            await asyncio.sleep(REQ_DELAY)
            contributors = await call_github_api_contributor(suffix_url=repository_name, github_id=github_id, page=page)

            if 'error' in contributors:
                raise HTTPException(status_code=404, detail=f"Contributors in {repository_name} not found")

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
    readme = await call_github_api_detail(suffix_url=f'{repository_name}/readme', github_id=github_id)
    has_readme = True if 'error' not in readme else False

    await asyncio.sleep(REQ_DELAY)
    latest_release = await call_github_api_detail(suffix_url=f'{repository_name}/releases/latest', github_id=github_id)
    release_version = latest_release.get('tag_name', None) if 'error' not in latest_release else None

    # Handle the license information
    license_info = repository_data.get("license")
    license_name = license_info.get("name") if license_info else None

    repository_item = {
        'id': repository_data.get("id"),
        'name': repository_data.get("name"),
        'url': repository_data.get("html_url"),
        'owner_github_id': repository_data.get("owner", {}).get("login"),
        'default_branch': repository_data.get("default_branch"),
        'created_at': repository_data.get("created_at"),
        'updated_at': repository_data.get("updated_at"),
        'pushed_at': repository_data.get("pushed_at"),
        'forked': repository_data.get('fork', False),
        'forks_count': repository_data.get("forks_count"),
        'stars_count': repository_data.get("stargazers_count"),
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
        'language_bytes': language_bytes,
        'contributors': contributors_list,
        'license': license_name,
        'has_readme': has_readme,
        'description': repository_data.get("description"),
        'release_version': release_version,
        'crawled_date': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    }

    print("-" * 10)
    print("api/repos")
    print(repository_item)
    return Response(content=json.dumps(repository_item), media_type="application/json")
# ------------------------ #

# -------------------- /repos/contributor ------------------------------#
@router.get('/contributor', response_class=Response)
async def get_repo_contributors(github_id: str, repo_name: str):
    contributors_list = []
    page = 1
    total_contributors_count = 0

    while True:
        await asyncio.sleep(REQ_DELAY)
        contributors = await call_github_api_contributor(suffix_url=repo_name, github_id=github_id, page=page)

        # If the response contains an error, raise an HTTPException
        if 'error' in contributors:
            raise HTTPException(status_code=404, detail=f"Contributors in {repo_name} not found")
        
        total_contributors_count += len(contributors)
        print(f"Page {page}: {len(contributors)} contributor(s)")

        for contributor in contributors:
            # Using `.get()` to handle possible missing keys or `None` values
            contributor_data = {
                'repo_url': f'{HTML_URL}/{github_id}/{repo_name}',
                'repository_url': f'{HTML_URL}/{github_id}/{repo_name}',
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

# -------------------- /repos/activity ------------------------------#
@router.get('/activity', response_class=Response)
async def get_repo_activity(github_id: str, repo_name: str, since: str, activity_type: str = 'all'):
    page = 1
    per_page = 100
    max_pages = 5
    normalized_type = activity_type.lower()
    if normalized_type not in ('all', 'issue', 'pr'):
        raise HTTPException(status_code=400, detail="activity_type must be one of all, issue, or pr")

    while page <= max_pages:
        await asyncio.sleep(REQ_DELAY)
        activity_items = await call_github_api_issue(
            suffix_url=repo_name,
            github_id=github_id,
            state='all',
            page=page,
            since=since,
            per_page=per_page,
        )

        if 'error' in activity_items:
            raise HTTPException(status_code=404, detail=f"Activity in {repo_name} not found")

        if not activity_items:
            break

        for item in activity_items:
            item_type = 'pr' if item.get('pull_request') else 'issue'
            if normalized_type in ('all', item_type):
                activity_data = {
                    'has_updates': True,
                    'latest_updated_at': item.get('updated_at'),
                    'latest_type': item_type,
                }
                return Response(content=json.dumps(activity_data), media_type="application/json")

        if len(activity_items) < per_page:
            break
        page += 1

    activity_data = {
        'has_updates': False,
        'latest_updated_at': None,
        'latest_type': None,
    }
    return Response(content=json.dumps(activity_data), media_type="application/json")
# ------------------------ #

# -------------------- /repos/snapshot ------------------------------#
@router.get('/snapshot', response_class=Response)
async def get_repo_snapshot(github_id: str, repo_name: str):
    collected_at = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

    await asyncio.sleep(REQ_DELAY)
    repository_data = await call_github_api_detail(suffix_url=repo_name, github_id=github_id)
    if 'error' in repository_data:
        raise HTTPException(status_code=404, detail=f"Repository {repo_name} not found")

    await asyncio.sleep(REQ_DELAY)
    languages = await call_github_api_detail(suffix_url=f'{repo_name}/languages', github_id=github_id)
    language_bytes = languages if 'error' not in languages else {}

    branches = []
    page = 1
    while True:
        await asyncio.sleep(REQ_DELAY)
        branch_page = await call_github_api_detail(
            suffix_url=f'{repo_name}/branches?page={page}&per_page=100',
            github_id=github_id,
        )
        if 'error' in branch_page or not branch_page:
            break
        branches.extend(branch_page)
        if len(branch_page) < 100:
            break
        page += 1

    await asyncio.sleep(REQ_DELAY)
    workflows = await call_github_api_detail(suffix_url=f'{repo_name}/contents/.github/workflows', github_id=github_id)
    workflow_files = []
    if isinstance(workflows, list):
        for item in workflows:
            path = item.get('path') or item.get('name') or ''
            if path.lower().endswith(('.yml', '.yaml')):
                workflow_files.append({
                    'path': path,
                    'size': item.get('size') or 0,
                })

    await asyncio.sleep(REQ_DELAY)
    readme = await call_github_api_detail(suffix_url=f'{repo_name}/readme', github_id=github_id)
    has_readme = 'error' not in readme
    dependency_evidence = dependency_evidence_from_readme(decode_github_content(readme)) if has_readme else {
        'matched_terms': [],
        'match_count': 0,
    }

    await asyncio.sleep(REQ_DELAY)
    dependabot_config = await call_github_api_detail(suffix_url=f'{repo_name}/contents/.github/dependabot.yml', github_id=github_id)
    if 'error' in dependabot_config:
        await asyncio.sleep(REQ_DELAY)
        dependabot_config = await call_github_api_detail(suffix_url=f'{repo_name}/contents/.github/dependabot.yaml', github_id=github_id)

    snapshot_data = {
        'repository_url': f'{HTML_URL}/{github_id}/{repo_name}',
        'collected_at': collected_at,
        'default_branch': repository_data.get('default_branch'),
        'branch_count': len(branches),
        'language_bytes': language_bytes,
        'language_percentage': calculate_language_percentage(language_bytes),
        'workflow_yaml_count': len(workflow_files),
        'workflow_yaml_total_size': sum(item.get('size') or 0 for item in workflow_files),
        'workflow_yaml_paths': [item.get('path') for item in workflow_files],
        'has_readme': has_readme,
        'readme_dependency_mentioned': dependency_evidence.get('match_count', 0) > 0,
        'dependency_evidence': dependency_evidence,
        'dependabot_config_present': 'error' not in dependabot_config,
    }
    return Response(content=json.dumps(snapshot_data), media_type="application/json")
# ------------------------ #

# -------------------- /repos/review-comments ------------------------------#
@router.get('/review-comments', response_class=Response)
async def get_repo_review_comments(github_id: str, repo_name: str, since: str = '2008-01-01T00:00:00Z'):
    review_comments = []
    page = 1
    max_pr_count = 200
    total_pr_count = 0

    while total_pr_count < max_pr_count:
        await asyncio.sleep(REQ_DELAY)
        pull_list = await call_github_api_pull(suffix_url=repo_name, github_id=github_id, state='all', page=page, since=since)
        if 'error' in pull_list or not pull_list:
            break

        total_pr_count += len(pull_list)
        for pull in pull_list:
            pr_number = pull.get('number')
            pr_id = str(pull.get('id')) if pull.get('id') is not None else None
            if pr_number is None:
                continue

            await asyncio.sleep(REQ_DELAY)
            reviews = await call_github_api_detail(suffix_url=f'{repo_name}/pulls/{pr_number}/reviews', github_id=github_id)
            if isinstance(reviews, list):
                for review in reviews:
                    review_comments.append({
                        'pr_id': pr_id,
                        'pr_number': pr_number,
                        'comment_id': str(review.get('id')),
                        'author_github_id': extract_login(review.get('user')),
                        'created_at': review.get('submitted_at'),
                        'updated_at': review.get('submitted_at'),
                        'path': None,
                        'position': None,
                        'comment_type': 'review',
                        'state': review.get('state'),
                    })

            await asyncio.sleep(REQ_DELAY)
            comments = await call_github_api_detail(suffix_url=f'{repo_name}/pulls/{pr_number}/comments', github_id=github_id)
            if isinstance(comments, list):
                for comment in comments:
                    review_comments.append({
                        'pr_id': pr_id,
                        'pr_number': pr_number,
                        'comment_id': str(comment.get('id')),
                        'author_github_id': extract_login(comment.get('user')),
                        'created_at': comment.get('created_at'),
                        'updated_at': comment.get('updated_at'),
                        'path': comment.get('path'),
                        'position': comment.get('position'),
                        'comment_type': 'comment',
                        'state': None,
                    })

        if len(pull_list) < 100:
            break
        page += 1

    return Response(content=json.dumps(review_comments), media_type="application/json")
# ------------------------ #

# -------------------- /repos/dependabot-alerts ------------------------------#
@router.get('/dependabot-alerts', response_class=Response)
async def get_repo_dependabot_alerts(github_id: str, repo_name: str):
    alerts = []
    page = 1

    while True:
        await asyncio.sleep(REQ_DELAY)
        alert_page = await call_github_api_detail(
            suffix_url=f'{repo_name}/dependabot/alerts?state=all&page={page}&per_page=100',
            github_id=github_id,
        )
        if 'error' in alert_page:
            if page == 1:
                return Response(
                    content=json.dumps({
                        'alerts': [],
                        'error': alert_page.get('error'),
                        'message': alert_page.get('message'),
                    }),
                    media_type="application/json",
                )
            break
        if not alert_page:
            break

        for alert in alert_page:
            dependency = alert.get('dependency') or {}
            package = dependency.get('package') or {}
            security_advisory = alert.get('security_advisory') or {}
            alerts.append({
                'github_alert_number': alert.get('number'),
                'state': alert.get('state'),
                'package_name': package.get('name'),
                'ecosystem': package.get('ecosystem'),
                'manifest_path': dependency.get('manifest_path'),
                'severity': security_advisory.get('severity'),
                'created_at': alert.get('created_at'),
                'fixed_at': alert.get('fixed_at'),
                'dismissed_at': alert.get('dismissed_at'),
                'collected_at': datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            })

        if len(alert_page) < 100:
            break
        page += 1

    return Response(content=json.dumps({'alerts': alerts}), media_type="application/json")
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
            issue_list = await call_github_api_issue(suffix_url=repo_name, github_id=github_id, state=state, page=page, since=since)
            
            # Handle potential errors or empty lists
            if 'error' in issue_list or not issue_list:
                break
            
            total_issue_count += len(issue_list)
            print(f'State: {state}')
            print(f"Page {page}: {len(issue_list)} issue(s)")

            for issue in issue_list:
                if issue.get('pull_request'):
                    continue
                issue_data = {
                    'id': issue.get('id'),
                    'issue_number': issue.get('number'),
                    'contributed_github_id': github_id,
                    'repo_url': f'{HTML_URL}/{github_id}/{repo_name}',
                    'repository_url': f'{HTML_URL}/{github_id}/{repo_name}',
                    'state': issue.get('state'),
                    'title': issue.get('title'),
                    'publisher_github_id': issue.get('user', {}).get('login', 'Unknown'),
                    'created_at': issue.get('created_at'),
                    'closed_at': issue.get('closed_at'),
                    'last_update': issue.get('updated_at')
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
            pull_list = await call_github_api_pull(suffix_url=repo_name, github_id=github_id, state=state, page=page, since=since)

            # Handle potential errors or empty lists
            if 'error' in pull_list or not pull_list:
                break
            
            total_pull_count += len(pull_list)
            print(f'State: {state}')
            print(f"Page {page}: {len(pull_list)} PR(s)")

            for pull in pull_list:
                pull_data = {
                    'id': pull.get("id"),
                    'pr_number': pull.get("number"),
                    'contributed_github_id': github_id,
                    'state': pull.get("state"),
                    'title': pull.get("title"),
                    'repo_url': f'{HTML_URL}/{github_id}/{repo_name}',
                    'repository_url': f'{HTML_URL}/{github_id}/{repo_name}',
                    'requester_id': pull.get('user', {}).get('login', 'Unknown'),
                    'created_at': pull.get('created_at'),
                    'closed_at': pull.get('closed_at'),
                    'merged_at': pull.get('merged_at'),
                    'merged_by': extract_login(pull.get('merged_by')),
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
async def get_commits(github_id: str, repo_name: str, since: str, include_files: bool = False):
    page = 1
    commits = []
    per_page = 100  
    max_pages = 2
    total_commit_count = 0

    try:
        while page <= max_pages:
            commit_list = await call_github_api_commit(suffix_url=repo_name, github_id=github_id, page=page, since=since, per_page=per_page)
            if 'error' in commit_list or not commit_list:
                break

            total_commit_count += len(commit_list)
            print("-"*20)
            print(f"Page {page}: {len(commit_list)} commit(s)")

            for commit in commit_list:
                sha = commit["sha"]
                await asyncio.sleep(REQ_DELAY)
                commit_detail = await call_github_api_commit_detail(suffix_url=repo_name, github_id=github_id, sha=commit["sha"])
                if 'stats' not in commit_detail or 'commit' not in commit_detail or 'author' not in commit_detail['commit']:
                    commit_detail = {
                        'stats': {'additions': 0, 'deletions': 0},
                        'commit': {'author': {'date': 'Unknown'}}
                    }

                committed_at = commit_detail['commit']['author'].get('date', 'Unknown')
                commit_data = {
                    'sha': sha,
                    'repository_url': f'{HTML_URL}/{github_id}/{repo_name}',
                    'contributed_github_id': github_id,
                    'author_github_id': commit['author']['login'] if commit['author'] else 'Unknown',
                    'added_lines': commit_detail['stats'].get('additions', 0),
                    'deleted_lines': commit_detail['stats'].get('deletions', 0),
                    'committed_at': committed_at,
                    'last_update': committed_at,
                }
                if include_files:
                    commit_data['files'] = [
                        classify_file_change(file_payload, committed_at)
                        for file_payload in commit_detail.get('files', [])
                    ]
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
