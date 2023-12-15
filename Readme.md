# Weather Service Application

## Description
This Weather Service Application is a Flask-based web service that provides weather information through the OpenWeatherMap API. It offers endpoints to fetch weather data based on city names, coordinates, and specific times.

## Prerequisites
Before you begin, ensure you have met the following requirements:
* You have a machine with Ubuntu 20.04.
* You have basic knowledge of Docker and Flask.

## Installation

### Docker Installation on Ubuntu 20.04
To install Docker on Ubuntu 20.04, follow these steps:

1. **Update the Package List**

   ```bash
   sudo apt update
   ```

2. **Install Required Packages**

   ```bash
   sudo apt install apt-transport-https ca-certificates curl software-properties-common
   ```

3. **Add Docker’s Official GPG Key**

   ```bash
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
   ```

4. **Add the Docker Repository**

   ```bash
   sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
   ```

5. **Install Docker Engine**

   ```bash
   sudo apt update
   sudo apt install docker-ce
   ```

6. **Verify Docker Installation**

   ```bash
   sudo systemctl status docker
   ```

   The service should be active and running.

### Application Setup

1. **Clone the Repository**

   Clone the repository to your local machine.

   ```bash
   git clone https://github.com/ncbateman/weather
   ```

2. **Navigate to the Application Directory**

   ```bash
   cd weather
   ```

## Usage

The application can be built, run, and tested using the provided scripts.

### Build Script

1. **Build the Docker Image**

   Use the `build.sh` script to build the Docker image for the application.

   ```bash
   ./scripts/bash/build.sh
   ```

   This will create a Docker image with all necessary dependencies installed.

### Run Script

1. **Run the Application**

   Use the `run.sh` script to start the application in a Docker container.

   ```bash
   ./scripts/bash/run.sh
   ```

   This will start the Flask application inside a Docker container. The API will be accessible at `localhost:8080`.

### Test Script

1. **Run Tests**

   Use the `test.sh` script to execute the tests for the application.

   ```bash
   ./scripts/bash/test.sh
   ```

   This will run the unit tests in a Docker container and display the test results.

## API Usage

After running the application, the following endpoints will be available:

- `GET /ping/`: A health check endpoint that returns the status of the application.
- `GET /forecast/<city_name>/?at=<ISO-8061 datetime>`: Fetches weather data for the specified city. The optional `at` parameter can be used to retrieve weather information at a specific time (in ISO-8601 format).

## Support

For support, contact the maintainer or submit an issue in the [GitHub repository](https://github.com/ncbateman/weather).

## License

This project is licensed under the [MIT License](LICENSE).
