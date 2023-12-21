FROM python:3.9-slim

RUN apt-get update && apt-get install -y pkg-config python3-dev default-libmysqlclient-dev build-essential \
    && apt-get clean

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 80

ENTRYPOINT ["streamlit", "run", "src/Accueil.py", "--server.address=0.0.0.0"]