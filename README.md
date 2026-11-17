# AI Agent – Inventory Assistant

A Django chat app where a Google Gemini agent manages a small warehouse inventory
(check stock, add/remove items, set prices, calculate cost with VAT) by calling tools.

## Requirements

- Docker
- A Gemini API key (https://aistudio.google.com/apikey)

## Run the image from GitHub

```bash
docker pull ghcr.io/jad-lakkis/ai-agent:latest
docker run -d --name ai-agent -p 8000:8000 -e GEMINI_API_KEY=your-key-here ghcr.io/jad-lakkis/ai-agent:latest
```

Open http://localhost:8000/

The image is built and pushed to the GitHub Container Registry automatically by
`.github/workflows/ci-cd.yml` on every push to `main`.

## CI/CD pipeline

`.github/workflows/ci-cd.yml` runs on every push to `main` (or manually from the
Actions tab) and has three jobs. Each one only starts if the previous one passed.

| Job | Runs on | What it does |
|---|---|---|
| `test` | GitHub-hosted Ubuntu | Installs dependencies, then runs `manage.py check`, a missing-migrations check and `manage.py test` |
| `build` | GitHub-hosted Ubuntu | Builds the Docker image and pushes it to `ghcr.io/jad-lakkis/ai-agent:latest` |
| `deploy` | Self-hosted runner (label `ai-agent-deploy`) | Pulls the new image and replaces the `ai-agent` container on port 8000 |

### One-time setup for the deploy job

1. **Secret:** in the repo go to Settings > Secrets and variables > Actions and add a
   repository secret named `GEMINI_API_KEY` (or run `gh secret set GEMINI_API_KEY`).
   The deploy job fails with a clear message if it is missing.
2. **Runner:** on the machine that should host the app (needs Docker running), go to
   Settings > Actions > Runners > New self-hosted runner, follow the download and
   `config` steps, and when asked for extra labels enter `ai-agent-deploy`.
   Then start it with `run.cmd` (Windows) or `./run.sh` (macOS / Linux).
3. Push to `main`. When the run finishes, open http://localhost:8000/ on the runner machine.

## Build and run locally

```bash
docker build -t ai-agent .
docker run -d --name ai-agent -p 8000:8000 -e GEMINI_API_KEY=your-key-here ai-agent
```

Stop and remove the container:

```bash
docker rm -f ai-agent
```

## Notes

- The API key is passed at run time and is never stored in the image or the repository.
- The SQLite database lives inside the container, so the inventory resets when the
  container is removed.
- Django admin: http://localhost:8000/admin/ (create a user with
  `docker exec -it ai-agent python manage.py createsuperuser`).

## Run without Docker

Requires Python 3.12+.

```bash
pip install -r requirements.txt
echo GEMINI_API_KEY=your-key-here > .env
python manage.py migrate
python manage.py runserver
```
