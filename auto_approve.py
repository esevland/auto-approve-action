#!/usr/bin/env python
# -*- encoding: utf-8

import json
import os
import sys

import requests

from github import Github
from github.Repository import Repository

GITHUB_TOKEN = os.getenv("INPUT_GITHUB_TOKEN")
GITHUB_EVENT_PATH = os.getenv("GITHUB_EVENT_PATH")
GITHUB_EVENT_NAME = os.getenv("GITHUB_EVENT_NAME")
INPUT_COMMENT = os.getenv("INPUT_COMMENT")

class ApprovePullRequest:
    """Approve GitHub pull request"""

    def __init__(self) -> None:
        if not GITHUB_TOKEN:
            print(f"Missing GITHUB_TOKEN")
            sys.exit(0)

        self.github = Github(GITHUB_TOKEN)
        self.event_json = None

        self._read_event_path_data()

    def _read_event_path_data(self) -> None:
        """Read JSON payload from GitHub event trigger

        An Action workflow runs in an environment with some default
        environment variables. A lot of convenient information is
        available here, including event data. The most complete way
        to access the event data is using the $GITHUB_EVENT_PATH variable,
        the path of the file with the complete JSON event payload.

        :return: no value
        :rtype: none
        """
        with open(GITHUB_EVENT_PATH) as json_file:
            event_json = json.load(json_file)
        self.event_json = event_json

    def get_repo_object(self) -> Repository:
        """Fetch Repository() object by parsing event data

        :return: github.Repository.Repository
        :rtype: Class
        """
        repo_name = self.event_json["repository"]["full_name"]
        org, repo = repo_name.split("/")
        org_object = self.github.get_organization(org)
        repo_object = org_object.get_repo(repo)
        return repo_object

    def main(self) -> None:
        """main"""
        pull_request = None
        repo = self.get_repo_object()
        comment = INPUT_COMMENT

        if GITHUB_EVENT_NAME == "pull_request":
            pull_request = repo.get_pull(self.event_json["number"])
        else:
            push_head = self.event_json["after"]
            for pr in repo.get_pulls():
                if push_head == pr.head.sha:
                    pull_request = pr

        if not pull_request:
            print("Pull request not found.")
            sys.exit(0)

        pup = requests.get("https://dog.ceo/api/breeds/image/random").json()["message"]
        pull_request.create_issue_comment(f'<p align="center"><img src="{pup}"></p>')
        pull_request.create_review(body=comment, event="APPROVE")


if __name__ == "__main__":
    approve_pr = ApprovePullRequest()
    approve_pr.main()
