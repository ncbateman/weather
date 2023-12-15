# Use the weather base image.
FROM weatherbase:latest

# Install required testing libraries
RUN pip3 install --default-timeout=1000 --ignore-installed pytest
RUN pip3 install --default-timeout=1000 --ignore-installed Flask-Testing
RUN pip3 install --default-timeout=1000 --ignore-installed requests-mock

# Set working directory
WORKDIR /app

# Copy the necessary files from host to container
# Ensure you copy all necessary files and folders like tests, src, etc.
COPY . .

# Command to run when the container starts
CMD ["pytest"]
