FROM python:3.11-slim
WORKDIR /app
COPY requirements-dev.txt /app/requirements-dev.txt
COPY packages /app/packages
COPY apps /app/apps
COPY configs /app/configs
COPY examples /app/examples
RUN pip install --no-cache-dir -r requirements-dev.txt && pip install -e packages/xr_privacy_sdk
EXPOSE 8080
CMD ["uvicorn", "apps.server.main:app", "--host", "0.0.0.0", "--port", "8080"]
