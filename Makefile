run_flask:
	python3 app/main.py

service:
	cp docker-compose-leds.service /etc/systemd/system/.

build:
	docker-compose up -d

.PHONY: run_flask service build
