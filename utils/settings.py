import asyncio
import httpx

# URL
API_URL = 'https://api.github.com'
HTML_URL = 'https://github.com'
GITHUB_TOKEN_FILE = 'GITHUB_TOKEN'
remaining_requests = 0
current_token = None
REQ_DELAY = 1

async def get_github_tokens():
   try:
       with open(GITHUB_TOKEN_FILE, 'r') as file:
           github_tokens = [line.strip() for line in file if line.strip()]
       return github_tokens
   except FileNotFoundError:
       print("Error: github_token_file_not_found")
       raise Exception("github_token_file_not_found")
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
           print("Error: authentication_failed_invalid_token")
           raise Exception("authentication_failed_invalid_token")
       else:
           print(f"Error fetching rate limit: {e.response.status_code}")
           raise Exception(f"rate_limit_fetch_failed_status_{e.response.status_code}")
   except httpx.RequestError as e:
       print(f"Network error while fetching rate limit: {e}")
       raise Exception("network_error_rate_limit_fetch")
   except Exception as e:
       print(f"Unexpected error in check_rate_limit: {e}")
       raise

async def get_new_token():
   global remaining_requests, current_token
   try:
       github_tokens = await get_github_tokens()
       
       for token in github_tokens:
           try:
               remaining_requests = await check_rate_limit(token)
               if remaining_requests > 0:
                   current_token = token
                   return token
           except Exception as e:
               print(f"Warning: Token {token} failed - {e}")
       
       raise Exception("all_tokens_exhausted")
   except Exception as e:
       print(f"Error getting new token: {e}")
       raise