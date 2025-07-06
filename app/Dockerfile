FROM python:3.9-slim

WORKDIR /code


RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

CMD ["python", "main.py"]