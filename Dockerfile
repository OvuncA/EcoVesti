# Official Slim Python Image
FROM python:3.11.9-slim

# Install git and other dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# Expose the port of the Flask app runs on (usually 5000)
EXPOSE 5000

# Run the gunicorn command to start your Flask application
CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "main:app" ]