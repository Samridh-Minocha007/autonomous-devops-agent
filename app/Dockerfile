FROM python:3.9-slim

WORKDIR /code


RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install -r requirements.txt


COPY . .

CMD ["python", "main.py"]