# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11-slim

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /app
COPY . /app

EXPOSE 8000
ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
