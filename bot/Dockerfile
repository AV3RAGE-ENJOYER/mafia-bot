FROM python:latest
WORKDIR /usr/share/mafia_app/
COPY . .
RUN pip install -r requirements.txt
RUN pip install -e .
WORKDIR /usr/share/mafia_app/mafia/
CMD ["python", "main.py"]