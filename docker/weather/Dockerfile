# Use the official Ubuntu image as a parent image
FROM weatherbase:latest

# Set working directory
WORKDIR /app

# Copy the necessary files from your host to the container
COPY src/ ./src/

# Command to run when the container starts
CMD ["python3", "/app/src/app.py"]
