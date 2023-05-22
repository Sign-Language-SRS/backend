backend-build:
	docker build -t ehuan2/srs-backend:latest -f Dockerfile ./src

run:
	docker-compose up

.PHONY: clean
clean:
	rm *.o

build: backend-build