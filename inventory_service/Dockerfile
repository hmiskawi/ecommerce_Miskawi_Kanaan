# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all application files to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir flask requests

# Expose the port used by the service
EXPOSE 5002

# Default command to run the inventory service
CMD ["python", "inventory.py"]
