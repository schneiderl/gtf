import git
import os
from os.path import expanduser
from github import Github
import requests

g = Github(os.environ['GITHUB_OAUTH'])

def createForkFromUserRepo(username, repo):
    user = g.get_user()
    owner_user = g.get_user(username)
    repo = owner_user.get_repo(repo)
    return user.create_fork(repo)

def creteForkFromOrgRepo(organization, repo):
    user = g.get_user()
    owner_organization = g.get_user(organization)
    repo = owner_organization.get_repo(repo)
    return user.create_fork(repo)

def commitAllChangedFiles(path, commitMessage, author):
    repo = git.Repo(path)
    files = repo.git.diff(None, name_only = True )
    for f in files.split('\n'):
        repo.git.add(f)
    repo.git.commit("-m", commitMessage, author = author)

def cloneRepo(url):
    repo_name = url.rsplit('/', 1)[1]
    return git.Repo.clone_from(url, os.getcwd() + "/" + repo_name, branch="master")

def getJsonFromRepos(url):
    r = requests.get(url)
    return r.json()