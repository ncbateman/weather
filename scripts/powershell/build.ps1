docker build -f ./docker/base/Dockerfile -t weatherbase:latest .
docker build -f ./docker/weather/Dockerfile -t weather:latest .