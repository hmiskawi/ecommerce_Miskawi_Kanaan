# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all application files to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the ports used by the services
EXPOSE 5001 5005

# Default command to run both services
CMD ["sh", "-c", "python customers.py & python wishlist.py"]
