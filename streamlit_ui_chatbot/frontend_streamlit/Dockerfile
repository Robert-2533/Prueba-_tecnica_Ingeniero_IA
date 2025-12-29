FROM python:3.12-trixie

WORKDIR /frontend

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

CMD ["streamlit", "run", "/frontend/chat_ui.py"]



