docker stop weather
docker rm weather
docker build -f ./docker/weather/Dockerfile -t weather:latest .
docker run --name weather weather:latest