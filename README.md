# DevOps Practical · Delivery Lab

[![Pull request CI](https://github.com/arturasryan919-spec/DevopsPractical/actions/workflows/ci.yml/badge.svg?branch=main&event=pull_request)](https://github.com/arturasryan919-spec/DevopsPractical/actions/workflows/ci.yml?query=event%3Apull_request)
[![Main push pipeline](https://github.com/arturasryan919-spec/DevopsPractical/actions/workflows/ci.yml/badge.svg?branch=main&event=push)](https://github.com/arturasryan919-spec/DevopsPractical/actions/workflows/ci.yml?query=event%3Apush)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Container-Docker-2496ED?logo=docker&logoColor=white)

A portfolio-friendly DevOps lab built around a small Flask service. The app stays focused so the delivery work is easy to see: review a change, run checks, build and publish a container image, then deploy it with Docker Compose.

## What this lab demonstrates

- A responsive service dashboard with environment and release details.
- A JSON health probe for the container and deployment workflow.
- A non-root Docker image served by Gunicorn.
- Pull request checks on GitHub-hosted runners.
- Commit-tagged container publishing to Docker Hub after changes reach `main`.
- Deployment from `main` on a self-hosted runner, followed by a container health check and HTTP probe.

## Delivery flow

```mermaid
flowchart LR
    PR["Pull request to main"] --> CI["GitHub-hosted CI"]
    CI --> TEST["pytest"]
    TEST --> BUILD["Docker build"]
    BUILD -->|merge to main| HUB["Publish commit tag + latest"]
    HUB --> RUNNER["Self-hosted runner"]
    RUNNER --> COMPOSE["Docker Compose deploy"]
    COMPOSE --> HEALTH["Container health + HTTP probe"]
```

The publish and deploy steps run only for a push to `main`. Pull requests run the tests and build the image without using Docker Hub credentials or the self-hosted runner.

The **Pull request CI** badge tracks the checks that run for pull requests. The **Main push pipeline** badge tracks publishing and deployment too, so its status depends on the self-hosted runner being online.

## Run locally

Requirements: Docker Engine with the Compose plugin.

```bash
APP_ENV=local docker compose up --build -d
```

Open [http://localhost:5000](http://localhost:5000), then try:

- `GET /` — the service dashboard.
- `GET /health` — container health response.
- `GET /api/status` — environment and release details as JSON.

Useful commands:

```bash
docker compose ps
docker compose logs -f app
docker compose down
```

Set a different host port with `APP_PORT=5080 APP_ENV=local docker compose up --build -d`.

## Run tests without Docker

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r app/requirements.txt
python -m pip install pytest
PYTHONPATH=. python -m pytest
```

## CI/CD setup

The workflow in [`.github/workflows/ci.yml`](.github/workflows/ci.yml) expects:

1. GitHub Actions repository secrets `DOCKER_USERNAME` and `DOCKER_PASSWORD`. Use a Docker Hub access token for the password.
2. A self-hosted GitHub Actions runner with the `self-hosted` label, Docker Engine, and the Docker Compose plugin.
3. Port `5000` available on the deployment host.

Pull request jobs run on GitHub-hosted runners. The self-hosted runner is used only after CI passes on a push to `main`. Keep that runner restricted to this trusted repository.

### Start the self-hosted runner in WSL

The deployment job needs the WSL runner online. If WSL is shut down or the runner process is stopped, GitHub cannot assign the job; it will wait for an available runner.

1. Open the WSL distribution where the GitHub Actions runner was configured.
2. In its terminal, go to the runner's installation folder (the example below assumes `~/actions-runner`):
   ```bash
   cd ~/actions-runner
   ./run.sh
   ```
3. Keep that terminal open. Confirm it says **Listening for Jobs**, then check the repository's **Settings → Actions → Runners** page shows the runner as **Online** or **Idle**.

When the runner returns online, a job that is still queued should start automatically. If the deployment job has already failed, bring the runner online first, then re-run the failed job from the Actions page.

## A short interview introduction

> I built this lab to practice taking a change from pull request through automated tests and a container build, then publishing a commit-tagged image and deploying it with Docker Compose. The service includes a health endpoint so the deployment can verify the running container.

## Next steps

- Add a staging environment before production deployment.
- Add an explicit rollback workflow that deploys a selected commit tag.
- Add deployment notifications and basic runtime metrics.
