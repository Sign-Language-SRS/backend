backend-build:
	docker build -t ehuan2/srs_backend:latest -f Dockerfile ./src

run:
	docker compose --env-file .env up

.PHONY: clean
clean:
	rm *.o

build: backend-build