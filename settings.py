import json
# URL
API_URL = 'https://api.github.com'
HTML_URL = 'https://github.com'
# --------------------------------- #
HTTP_COMMIT = '#repo-content-pjax-container > div > div > div.Layout.Layout--flowRow-until-md.react-repos-overview-margin.Layout--sidebarPosition-end.Layout--sidebarPosition-flowRow-end > div.Layout-main > react-partial > div > div > div.Box-sc-g0xbh4-0.yfPnm > div:nth-child(1) > table > tbody > tr.Box-sc-g0xbh4-0.jEbBOT > td > div > div.Box-sc-g0xbh4-0.jGfYmh > a > span > span:nth-child(2) > span'
HTTP_OPEN_ISSUE = 'a[data-ga-click="Issues, Table state, Open"]'
HTTP_CLOSED_ISSUE = 'a[data-ga-click="Issues, Table state, Closed"]'


# --------------------------------- #

def get_github_token():
    with open('GITHUB_TOKEN', 'r') as file:
        return file.readline().strip()

def response(data):
    return json.dumps(data, indent=4)