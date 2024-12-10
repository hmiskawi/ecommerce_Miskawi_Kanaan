# Use a lightweight base image with SQLite
FROM alpine:latest

# Install SQLite
RUN apk add --no-cache sqlite

# Set the working directory
WORKDIR /app

# Copy the database file into the container
COPY ./ecommerce.db /app/ecommerce.db

# Command to start SQLite in server mode (if applicable)
CMD ["sqlite3", "/app/ecommerce.db"]
