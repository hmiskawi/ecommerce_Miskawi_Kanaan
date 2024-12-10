# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all application files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir flask requests

# Expose the ports used by the services
EXPOSE 5004 5006

# Command to run both reviews and auth services
CMD ["sh", "-c", "python reviews.py & python auth.py"]
