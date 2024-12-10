# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy all the application files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir flask flask-cors werkzeug

# Expose the port the app runs on
EXPOSE 5000

# Initialize the database on container startup
CMD ["python", "ecommerce_db.py"]
