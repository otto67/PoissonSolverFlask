FROM python:3

WORKDIR /usr/src/app
ENV FLASK_APP main.py
COPY main.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "main.py"]