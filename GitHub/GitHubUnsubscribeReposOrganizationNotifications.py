#!/usr/bin/env python
import os

from github import Github
from github.Organization import Organization
from github.PaginatedList import PaginatedList
from github.Repository import Repository
from github.AuthenticatedUser import AuthenticatedUser


g = Github(os.getenv("github_api_token"))

user:AuthenticatedUser = g.get_user()

organization:Organization = g.get_organization(os.getenv("github_organization"))

repositories:PaginatedList = organization.get_repos()


print(str(repositories.totalCount) + " found.")
confirmation = input("Do you want to process it? (y/n)")

if confirmation not in ["y", "Y", "s", "S"]:
    exit(0)

confirmation_needed = input("Do you want to confirm each change? (y/n)")


processed = 0
for repo in repositories:
    repo:Repository = repo
    if confirmation_needed in ["y", "Y", "s", "S"]:
        y = input("Do you want to stop watching '{name}'? (y/n)".format(name=repo.full_name))
    else:
        y = "y"

    if y in ["y", "Y", "s", "S"]:
        user.remove_from_watched(repo)
        processed += 1


print(str(processed) + " repositories processed!")
