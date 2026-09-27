Kaagaz is a Flask app with a SQLite file, so it runs anywhere Python runs.
This is the no-platform-lock-in path; Vercel (serverless) is configured in
vercel.json and deployed by .github/workflows/deploy.yml.

# Multi-stage: gunicorn in the final image, build tools never ship.
FROM python:3.11-slim AS build
WORKDIR /app
RUN pip install --no-cache-dir gunicorn
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

FROM python:3.11-slim
WORKDIR /app

# Run as an unprivileged user.
RUN useradd --create-home --uid 10001 kaagaz

COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build /usr/local/bin/gunicorn /usr/local/bin/gunicorn
COPY . .

# The database lives on a volume so it survives container restarts. Point
# DATABASE_PATH elsewhere to put it somewhere else.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000 \
    DATABASE_PATH=/data/kaagaz.db

# /data is created up front and handed to the unprivileged user, because a
# fresh volume mounts as root and the app would otherwise fail to write.
RUN mkdir -p /data && chown -R kaagaz:kaagaz /data /app
VOLUME ["/data"]

USER kaagaz
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/api/research/health', timeout=4).status==200 else 1)"

# One worker on purpose. The app is a single-process SQLite app with a
# threadpool of fetchers inside each request; scaling out means migrating off
# SQLite, which is a different project. A thread pool is what this needs, and
# gthread is the worker class that uses it.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "--threads", "8", \
     "--timeout", "180", "--graceful-timeout", "30", "wsgi:app"]
