FROM python:3.12-slim
WORKDIR /app
# Same dependencies as pyproject.toml; uvicorn[standard] adds the fast WebSocket/HTTP stack.
RUN pip install --no-cache-dir "fastapi>=0.115" "requests>=2.31" "python-multipart>=0.0.9" "uvicorn[standard]>=0.30" "websockets>=13"
COPY app ./app
# GNANI_API_KEY comes from the host's secret settings at runtime; it is never baked into the image.
ENV PORT=8000
EXPOSE 8000
CMD ["sh", "-c", "exec uvicorn app.server:app --host 0.0.0.0 --port $PORT --proxy-headers --forwarded-allow-ips='*'"]
