import os
import sys
from github import Github
from misspellings import misspelling_dict
from git import Repo
import file_handler
import github_connector
import subprocess


g = Github(os.environ['GITHUB_OAUTH'])
user = g.get_user()

owner_organization = g.get_user(sys.argv[1])
repos = owner_organization.get_repos()

print("Working :). Wait a few minutes.")

for repo in repos:
    try:
        readme = repo.get_readme().decoded_content
        text = readme.decode()
        repo_cloned = False
        for line in text.split('\n'):
            words = line.split(" ")
            for word in words:
                if (word in misspelling_dict):
                    print("Possible misspeling at " +
                          repo.full_name + '. Word: ' + word)
                    if (repo_cloned is False):
                        print("creating fork")
                        forked_repo = user.create_fork(repo)
                        print("Cloning repo at ./" + forked_repo.full_name)
                        Repo.clone_from(
                            "https://github.com/" +
                            forked_repo.full_name, "./" +
                            forked_repo.full_name)

                        repo_cloned = True
                    print("Repo cloned. Fixing misspellings")
                    file_handler.fixTypos(
                        "./" + forked_repo.full_name +
                        "/README.md", word,
                        misspelling_dict[word][0])

        if (repo_cloned is True):
            print("Commit for " + repo.full_name)
            push_process = subprocess.Popen(["git", "checkout -b fix_typo"], cwd = "./" + forked_repo.full_name)
            github_connector.commitAllChangedFiles(
                "./" + forked_repo.full_name,
                "Fix typos in readme.md",
                "Lucas Schneider <casdpa@gmail.com>")
            print("Pushing changes to " + forked_repo.full_name)
            push_process = subprocess.Popen(["git", "push"], cwd = "./" + forked_repo.full_name)


            push_process.wait()
    
    except Exception as x:
        print(x)
        pass

print("Finished.")
