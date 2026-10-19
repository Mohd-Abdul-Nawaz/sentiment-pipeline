.PHONY: install run test producer consumer up down

install:
	pip install -r requirements.txt

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

up:
	docker-compose up --build

down:
	docker-compose down

test:
	pytest tests/ -v

producer:
	python app/producer.py

consumer:
	python app/consumer.py