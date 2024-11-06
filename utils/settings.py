import asyncio
import httpx

API_URL = 'https://api.github.com'
HTML_URL = 'https//github.com'
GITHUB_TOKEN_FILE = 'GITHUB_TOKEN'
remaining_requests = 0
current_token = None
REQ_DELAY = 0.5

async def get_github_tokens():
    with open(GITHUB_TOKEN_FILE, 'r') as file:
        tokens = [line.strip() for line in file if line.strip()]
    return tokens

async def check_rate_limit(token):
    url = f"{API_URL}/rate_limit"
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            rate_limit_info = response.json()
            remaining_requests = rate_limit_info['rate']['remaining']
            return remaining_requests
        elif response.status_code == 401:
            raise Exception("Authentication failed: Invalid token")
        else:
            raise Exception(f"Error fetching rate limit: {response.status_code}")

async def get_new_token():
    global remaining_requests, current_token
    tokens = await get_github_tokens()
    
    for token in tokens:
        remaining_requests = await check_rate_limit(token)
        if remaining_requests > 0:
            current_token = token
            return token
    raise Exception("All tokens are exhausted")
