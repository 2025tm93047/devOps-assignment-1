# ACEest Fitness DevOps Assignment

This repository contains the Flask implementation and CI/CD configuration for Introduction to DevOps Assignment 1. The app supports an authenticated fitness dashboard, client registration, workout-program generation, workout logging, and a JSON health/client API. The automated pipelines compile and test the app, build its Docker image, and verify a running container's health endpoint.

## Source adaptation

The supplied archive contains Tkinter desktop implementations, including `Aceestver-3.2.4.py`. This submission preserves the fitness-management concepts while implementing the required Flask web application so it can be tested and built consistently through Docker, Jenkins, and GitHub Actions.

## Run locally on Windows

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:ADMIN_USERNAME = "admin"
$env:ADMIN_PASSWORD = "change-me"
python app.py
```

Open `http://127.0.0.1:5000`. The app creates its SQLite database under `instance/`. Set a unique `ADMIN_PASSWORD` before exposing the app beyond a local demo.

## Run tests

```powershell
python -m pytest -q
```

The tests cover the health endpoint, the authentication boundary, client creation and duplicate rejection, program generation, workout logging, and client detail API.

## Build and run with Docker

```powershell
docker build --tag aceest-fitness-devops:local .
docker run --detach --rm --name aceest-fitness `
  --publish 5000:5000 `
  --env ADMIN_PASSWORD=change-me `
  --volume aceest-data:/app/instance `
  aceest-fitness-devops:local
```

Check `http://127.0.0.1:5000/healthz`; a healthy app returns `{"service":"aceest-fitness","status":"ok"}`. The image uses a non-root account and declares a Docker health check. Stop the demo container with `docker stop aceest-fitness`.

## GitHub Actions

`.github/workflows/main.yml` runs on each push and pull request. It builds the Docker image, compiles the application inside that image, runs Pytest inside the image, and starts a smoke-test container to verify `/healthz`.

## Jenkins BUILD job

Create a Jenkins Pipeline job using **Pipeline script from SCM**, set the public GitHub repository URL, select Git, and keep `Jenkinsfile` as the script path. The Jenkins agent needs Python 3 and a working Docker CLI/daemon. The pipeline checks out the configured revision, installs the Python requirements in a workspace virtual environment, runs Pytest, builds the image, runs the container health check, and cleans up its temporary container/image. Jenkins marks the Docker stage unsuccessful and the build unstable if the agent cannot access Docker; it does not report a Docker build as successful when none ran.

Keep credentials in Jenkins credential storage and never commit passwords, tokens, or local environment files.
