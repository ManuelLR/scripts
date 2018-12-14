#!/usr/bin/env python
import os

from github import Github
from github.Hook import Hook
from github.Organization import Organization
from github.PaginatedList import PaginatedList
from github.Repository import Repository
from github.AuthenticatedUser import AuthenticatedUser

# Configuration

github_api_token = os.getenv("github_api_token")
github_organization = os.getenv("github_organization")

desired_hook_config = {
    "url": os.getenv("jenkins_github_url"),
    "content_type": "json",
    "secret": os.getenv("jenkins_github_secret"),
    "insecure_ssl": "0",
}
desired_hook_events = ["push"]
desired_hook_name = "web"

# Connection
g = Github(github_api_token)

user:AuthenticatedUser = g.get_user()

organization:Organization = g.get_organization(github_organization)

repositories:PaginatedList = organization.get_repos()


print(str(repositories.totalCount) + " found.")
confirmation = input("Do you want to process it? (y/n)")


if confirmation not in ["y", "Y", "s", "S"]:
    exit(0)

confirmation_needed = input("Do you want to confirm each change? (y/n)")


# Start process
processed = 0
for repo in repositories:
    repo:Repository = repo
    repo_hooks:PaginatedList = repo.get_hooks()
    created = False
    repo_hook_selected:Hook = None


    for repo_hook in repo_hooks:
        repo_hook:Hook = repo_hook
        if "web" not in repo_hook.name:
            repo_hook.delete()
        elif "jenkins.geographica" in repo_hook.config.get("url", ""):
            # hook_config: dict = repo_hook.config
            repo_hook_selected = repo_hook

    if confirmation_needed in ["y", "Y", "s", "S"]:
        y = input("Do you want to edit Jenkins hook '{name}'? (y/n)".format(name=repo.full_name))
    else:
        y = "y"

    if y in ["y", "Y", "s", "S"]:
        if repo_hook_selected:
            repo_hook_selected.edit(name=desired_hook_name, config=desired_hook_config, events=desired_hook_events)
        else:
            repo.create_hook(name=desired_hook_name, config=desired_hook_config, events=desired_hook_events)
        processed += 1


print(str(processed) + " repositories processed!")
