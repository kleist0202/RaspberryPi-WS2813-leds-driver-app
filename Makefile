USER :=

ifdef USER_ENV
    USER := $(USER_ENV)
else
    USER := $(shell whoami)
endif

run_flask:
	python3 app/main.py

install:
	cp ./docker-compose-leds@.service /etc/systemd/system/
	systemctl daemon-reload
	systemctl start docker-compose-leds@$(USER).service
	systemctl enable docker-compose-leds@$(USER).service

uninstall:
	systemctl disable docker-compose-leds@$(USER).service
	systemctl stop docker-compose-leds@$(USER).service
	rm /etc/systemd/system/docker-compose-leds@.service
	systemctl daemon-reload

build:
	docker-compose up -d

.PHONY: run_flask install uninstall build
