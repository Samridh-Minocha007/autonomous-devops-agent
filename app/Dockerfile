FROM python:3.9-slim

WORKDIR /code

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

CMD ["python", "main.py"]