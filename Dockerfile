FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 80

ENTRYPOINT ["streamlit", "run", "src/Accueil.py", "--server.port=80", "--server.address=0.0.0.0"]