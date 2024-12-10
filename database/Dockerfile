# Use a Python base image
FROM python:3.9-slim

# Install SQLite
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file first (helps with caching)
COPY requirements.txt /app/

# Install the Python dependencies listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app

# Command to run the Python script that interacts with SQLite
CMD ["python", "/app/ecommerce_db.py"]
