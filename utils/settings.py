import asyncio
import httpx

# URL
API_URL = 'https://api.github.com'
HTML_URL = 'https//github.com'
GITHUB_TOKEN_FILE = 'GITHUB_TOKEN'
remaining_requests = 0
current_token = None
REQ_DELAY = 0.5

async def get_github_tokens():
    try:
        with open(GITHUB_TOKEN_FILE, 'r') as file:
            tokens = [line.strip() for line in file if line.strip()]
        return tokens
    except FileNotFoundError:
        print("Error: GitHub token file not found.")
        raise Exception("GitHub token file not found.")
    except Exception as e:
        print(f"Error reading GitHub token file: {e}")
        raise

async def check_rate_limit(token):
    url = f"{API_URL}/rate_limit"
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()  # Raise exception for non-2xx responses
            rate_limit_info = response.json()
            remaining_requests = rate_limit_info['rate']['remaining']
            return remaining_requests
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            print("Error: Authentication failed - Invalid token")
            raise Exception("Authentication failed: Invalid token")
        else:
            print(f"Error fetching rate limit: {e.response.status_code}")
            raise Exception(f"Error fetching rate limit: {e.response.status_code}")
    except httpx.RequestError as e:
        print(f"Network error while fetching rate limit: {e}")
        raise Exception("Network error while fetching rate limit.")
    except Exception as e:
        print(f"Unexpected error in check_rate_limit: {e}")
        raise

async def get_new_token():
    global remaining_requests, current_token
    try:
        tokens = await get_github_tokens()
        
        for token in tokens:
            try:
                remaining_requests = await check_rate_limit(token)
                if remaining_requests > 0:
                    current_token = token
                    return token
            except Exception as e:
                print(f"Warning: Token {token} failed - {e}")
        
        raise Exception("All tokens are exhausted")
    except Exception as e:
        print(f"Error getting new token: {e}")
        raise