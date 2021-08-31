FROM python:3

ADD main.py ./main.py
ADD .env ./.env
COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt
CMD ["python", "main.py"]