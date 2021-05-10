FROM python:3

ADD OltovnyaBot/main.py ./main.py
ADD OltovnyaBot/.env ./.env
COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt
CMD ["python", "main.py"]