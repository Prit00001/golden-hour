FROM python:3.12-slim
WORKDIR /app
# Pinned: a rebuild can't silently pull a new, untested release. Bump on purpose, then rerun the tests.
RUN pip install --no-cache-dir fastapi==0.128.8 requests==2.32.5 python-multipart==0.0.20 "uvicorn[standard]==0.39.0" websockets==15.0.1
COPY app ./app
# GNANI_API_KEY comes from the host's secret settings at runtime; it is never baked into the image.
ENV PORT=8000 PYTHONDONTWRITEBYTECODE=1
EXPOSE 8000
USER nobody
# --ws-max-size: the largest message the page sends is the case JSON (a few KB); the default is 16 MB.
CMD ["sh", "-c", "exec uvicorn app.server:app --host 0.0.0.0 --port $PORT --proxy-headers --forwarded-allow-ips='*' --ws-max-size 65536 --no-server-header"]
