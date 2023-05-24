build: backend-build

backend-build:
	docker build -t ehuan2/srs_backend:latest -f Dockerfiles/backend .

run:
	docker compose --env-file .env up

.PHONY: clean
clean:
	rm -r **/__pycache__/**