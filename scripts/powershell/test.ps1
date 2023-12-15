docker build -f ./docker/base/Dockerfile -t weatherbase:latest .
docker stop weathertest
docker rm weathertest
docker build -f ./docker/test/Dockerfile -t weathertest:latest .
docker run --name weathertest weathertest:latest