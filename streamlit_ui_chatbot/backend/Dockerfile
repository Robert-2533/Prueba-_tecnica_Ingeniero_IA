FROM python:3.12-trixie

WORKDIR /backend

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

CMD ["uvicorn", "crud_fastAPI:app", "--host", "0.0.0.0", "--port", "54621", "--log-level", "debug"]



