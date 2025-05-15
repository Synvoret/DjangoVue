<!-- from run.sh -->
./run.sh

<!-- from Makefile -->
make start        # start all
make backend      # only backend
make frontend     # only frontend
make setup-venv   # make venv and install requirements

<!-- from Dockerfiles -->
docker/podman build -t app .
docker/podman run --rm -p 8000:8000 app
docker/podman build -t vue .
docker/podman run -it -p 5173:5173 --rm vue

<!-- from docker-compose -->
docker-compose/podman-compose up --build 
docker-compose/podman-compose ps
docker-compose/podman-compose down
