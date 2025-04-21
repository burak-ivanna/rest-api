ARG PYTHON_TAG=3.9-slim
FROM python:${PYTHON_TAG}

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["flask", "run", "--host=0.0.0.0"]