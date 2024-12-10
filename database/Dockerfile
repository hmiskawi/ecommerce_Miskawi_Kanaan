# Use Alpine as base image
FROM alpine:latest

# Install Python and SQLite
RUN apk add --no-cache python3 py3-pip sqlite

# Set the working directory inside the container
WORKDIR /app

# Copy the database file and the Python script
COPY ./ecommerce.db /app/ecommerce.db
COPY ./ecommerce_db.py /app/ecommerce_db.py

# Command to run the Python script that interacts with SQLite
CMD ["python3", "/app/ecommerce_db.py"]
