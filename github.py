import scrapy
import json

from ..settings import *
from ..items import *

class Gitspider(scrapy.Spider):
    name = 'github'
    token = get_github_token()
    custom_settings = save_into_json()

    def __init__(self, spider_type, *args, **kwargs):
        super(Gitspider, self).__init__(*args, **kwargs)
        self.spider_type = spider_type


    def start_requests(self):
        GithubIDs = ['johnkim6823']
        headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json',
        }
        # ------- USER -------#
        if self.spider_type == 'user':
            for GithubID in GithubIDs:
                url = f'{API_URL}/users/{GithubID}'
                yield scrapy.Request(url, headers=headers, callback=self.parse_user, meta={'GithubID': GithubID})

        # ------- REPO-------#
        elif self.spider_type == 'repo':
            for GithubID in GithubIDs:
                repos_url = f'{API_URL}/users/{GithubID}/repos'
                yield scrapy.Request(repos_url, headers=headers, callback=self.parse_repos, meta={'GithubID': GithubID})
        
        # ------- ISSUE -------#
        elif self.spider_type == 'issue':
            for GithubID in GithubIDs:
                repos_url = f'{API_URL}/users/{GithubID}/repos'
                yield scrapy.Request(repos_url, headers=headers, callback=self.parse_issues, meta={'GithubID': GithubID})

        # ------- PULL REQUEST -------#
        elif self.spider_type == 'pr':
            for GithubID in GithubIDs:
                repos_url = f'{API_URL}/users/{GithubID}/repos'
                yield scrapy.Request(repos_url, headers=headers, callback=self.parse_pulls, meta={'GithubID': GithubID})
        
         # ------- COMMIT -------#
        elif self.spider_type == 'commit':
            for GithubID in GithubIDs:
                repos_url = f'{API_URL}/users/{GithubID}/repos'
                yield scrapy.Request(repos_url, headers=headers, callback=self.parse_repos, meta={'GithubID': GithubID})
    
    # ------- USER PARSER -------#
    def parse_user(self, response):
        GithubID = response.meta['GithubID']
        student = json.loads(response.text)

        item = STUDENT()
        item['GithubID'] = student['login']
        item['Follower_CNT'] = student['followers']
        item['Following_CNT'] = student['following']
        item['Public_repos_CNT'] = student['public_repos']
        item['Github_profile_Create_Date'] = student['created_at']
        item['Github_profile_Update_Date'] = student['updated_at']
        item['email'] = student['email']
        item['Crawled_Date'] = datetime.now().strftime("%Y%m%d_%H%M%S")
        yield item

    # ------- REPO PARSER -------#
    def parse_repos(self, response):

        GithubID = response.meta['GithubID']
        repos = json.loads(response.text)
        
        for repo in repos:
            item = REPO()  # Assuming you have a REPO item defined similar to STUDENT
            item['RepoID'] = repo['id']
            item['RepoURL'] = repo['html_url']
            item['RepoNM'] = repo['name']
            item['OwnerGithubID'] = repo['owner']['login']
            item['CreationDate'] = repo['created_at']
            item['ForkCount'] = repo['forks_count']
            item['StarCount'] = repo['stargazers_count']
            item['OpenIssueCount'] = repo['open_issues_count']
            item['LicenseName'] = repo['license']['name'] if repo['license'] else None
            item['ProjectDescription'] = repo['description']

            print(item['RepoNM'])
            # Fetch additional data for each repository
            languages_url = f'{API_URL}/repos/{GithubID}/{repo["name"]}/languages'
            # print("--------------------")
            # print(f'{languages_url}')
            # print("--------------------")
            yield scrapy.Request(languages_url, headers=response.request.headers, callback=self.parse_languages, meta={'item': item, 'GithubID': GithubID, 'repo_name': repo["name"]})

    def parse_languages(self, response):
        item = response.meta['item']
        languages = json.loads(response.text) if response.text else {}
        item['ProgrammingLanguage'] = list(languages.keys()) if languages else None

        #Fetch contributors
        contributors_url = f'{API_URL}/repos/{response.meta["GithubID"]}/{response.meta["repo_name"]}/contributors'
        # print("--------------------")
        # print(f'{contributors_url}')
        # print("--------------------")
        yield scrapy.Request(contributors_url, headers=response.request.headers, callback=self.parse_contributors, meta={'item': item, 'GithubID': response.meta['GithubID'], 'repo_name': response.meta["repo_name"]})

    def parse_contributors(self, response):
        item = response.meta['item']
        contributors = json.loads(response.text) if response.text else []
        item['Contributors'] = [contributor['login'] for contributor in contributors if 'login' in contributor] if contributors else None
        
        # Fetch commits
        commits_url = f'{API_URL}/repos/{response.meta["GithubID"]}/{response.meta["repo_name"]}/commits?page=1&per_page=100'
        # print("--------------------")
        # print(f'{commits_url}')
        # print("--------------------")
        yield scrapy.Request(commits_url, headers=response.request.headers, callback=self.parse_commits, meta={'item': item, 'GithubID': response.meta['GithubID'], 'repo_name': response.meta["repo_name"]})


    def parse_commits(self, response):
        # Parsing the JSON response using json.loads instead of json.load
        commits_data = json.loads(response.text) if response.text else []
        commit_count = len(commits_data)
        
        # Updating the commit count in the item
        item = response.meta['item']
        item['CommitCount'] =  item.get('CommitCount', 0) + commit_count

        # If we've received less than 100 commits, we're on the last page
        if commit_count < 100:
            #We've reached the last page of commits, now proceed to fetch the README
            readme_url = f'{API_URL}/repos/{response.meta["GithubID"]}/{response.meta["repo_name"]}/readme'
            yield scrapy.Request(readme_url, headers=response.request.headers, callback=self.parse_readme, meta={'item': item, 'GithubID': response.meta['GithubID'], 'repo_name': response.meta["repo_name"]})
            
        else:
            # There might be more commits, fetch the next page
            current_page = response.meta.get('page',1)
            next_page = current_page + 1
            next_page_url = f'{API_URL}/repos/{response.meta["GithubID"]}/{response.meta["repo_name"]}/commits?page={next_page}&per_page=100'
            # print("--------------------")
            # print(f'{next_page_url}')
            # print("--------------------")
            yield scrapy.Request(next_page_url, headers=response.request.headers, callback=self.parse_commits, meta={'item': item, 'GithubID': response.meta['GithubID'], 'repo_name': response.meta['repo_name'], 'page': next_page})
    
    def parse_readme(self, response):
        item = response.meta['item']
        item['HasReadME'] = True if response.status == 200 else False
        yield item
        # Fetch release information
        release_url = f'{API_URL}/repos/{response.meta["GithubID"]}/{response.meta["repo_name"]}/releases/latest'
        # print("--------------------")
        # print(f'{release_url}')
        # print("--------------------")
        #yield scrapy.Request(release_url, headers=response.request.headers, callback=self.parse_release, meta={'item': item, 'GithubID': response.meta['GithubID'], 'repo_name': response.meta["repo_name"]})

    def parse_release(self, response):
        item = response.meta['item']
        if response.status == 200 and response.text:
            release = json.loads(response.text)
            item['ReleaseVersion'] = release['tag_name']
        else:
            # 응답이 200이 아니거나 응답 텍스트가 없는 경우에도
            # 'ReleaseVersion'을 None으로 설정합니다.
            item['ReleaseVersion'] = None
        
        # Now that all data is collected, yield the repo_item
        yield item
        
    # def parse_issues(self, response):
    #     issues = json.loads(response.text)
    #     for issue in issues:
    #         issue_item = ISSUE()
    #         issue_item['ISSUEID'] = issue['id']
    #         issue_item['IssuePublisherID'] = issue['user']['login']
    #         issue_item['OwnerGithubID'] = issue['repository']['owner']['login']
    #         issue_item['RepoURL'] = issue['repository_url']
    #         issue_item['IssueDate'] = issue['created_at']
    #         issue_item['Title'] = issue['title']
    #     yield issue_item

    # def parse_pulls(self, response):
    #     pulls = json.loads(response.text)
    #     for pr in pulls:
    #         pr_item = PR()
    #         pr_item['PRID'] = pr['id']
    #         pr_item['RequesterID'] = pr['user']['login']
    #         pr_item['OwnerGithubID'] = pr['head']['repo']['owner']['login']
    #         pr_item['RepoURL'] = pr['url']
    #         pr_item['PRDate'] = pr['created_at']
    #         pr_item['Title'] = pr['title']
    #     yield pr_item
