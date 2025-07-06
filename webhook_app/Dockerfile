FROM python:3.9-slim
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the app
COPY . .

CMD ["python", "main.py"]