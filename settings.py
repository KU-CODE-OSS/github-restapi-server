# URL
API_URL = 'https://api.github.com'
HTML_URL = 'https://github.com'
# --------------------------------- #

# --------------------------------- #

def get_github_token():
    with open('GITHUB_TOKEN', 'r') as file:
        return file.readline().strip()
