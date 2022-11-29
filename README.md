# :white_check_mark: auto-approve-action

A GitHub action to automatically approve pull requests.

:warning: For demonstration purposes only. Automatically approving pull requests is risky.

## Usage
```yaml
name: approve pull request

on:
  pull_request:
    branches:
      - main

jobs:
  approve_pr:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Approve Pull Request
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        uses: esevland/auto-approve-action@main
        with:
          body: ":shipit:"
```