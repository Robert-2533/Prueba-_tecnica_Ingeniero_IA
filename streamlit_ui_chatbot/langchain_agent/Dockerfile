# Usar una imagen base ligera de Python
FROM python:3.12-trixie

WORKDIR /temp

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

WORKDIR /agent

COPY . .


CMD ["uvicorn", "pipeline:app", "--host", "0.0.0.0", "--port", "8000"]