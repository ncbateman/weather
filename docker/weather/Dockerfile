# Use the weather base image.
FROM weatherbase:latest

# Set working directory
WORKDIR /app

# Copy the necessary files from host to container
COPY src/ ./src/

# Command to run when the container starts
CMD ["python3", "/app/src/app.py"]
