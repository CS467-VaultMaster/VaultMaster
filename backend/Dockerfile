FROM python:3.11-slim-bookworm

WORKDIR /backend

COPY requirements.txt /backend/requirements.txt

RUN pip install -r /backend/requirements.txt

COPY . /backend

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
