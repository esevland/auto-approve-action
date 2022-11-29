FROM python:3-slim AS builder

LABEL "com.github.actions.name"="Auto Approve"
LABEL "com.github.actions.description"="Automatically approve pull requests"
LABEL "com.github.actions.icon"="activity"
LABEL "com.github.actions.color"="green"

WORKDIR /action

RUN pip install --target=/action requests PyGithub
RUN apt-get update && apt-get install -y --no-install-recommends && apt-get purge -y --auto-remove && rm -rf /var/lib/apt/lists/*

ADD auto_approve.py /action
RUN chmod +x /action/auto_approve.py
CMD ["/action/auto_approve.py"]
