import httpx

TIMEOUT = 3600

# --- Request function --- #
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

