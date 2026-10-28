# Based on the EECE430 Docker tutorial Dockerfile.
# Python 3.13 instead of 3.11: this app uses Django 6.1, which needs Python 3.12+.
FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/

# Create the SQLite tables inside the image. Checks are skipped because they
# import chat/agent.py, which needs GEMINI_API_KEY (only given at run time).
RUN python manage.py migrate --noinput --skip-checks

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
