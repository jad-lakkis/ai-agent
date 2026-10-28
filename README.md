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
`.github/workflows/docker.yml` on every push to `main`.

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
