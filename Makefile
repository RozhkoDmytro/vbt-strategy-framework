rebuild:
	docker-compose down
	docker-compose build --no-cache
	docker-compose up --build

pytest:
	clear
	pytest -x $(ARGS)

run:
	python main.py

clean:
	chmod +x cleanup.sh
	./cleanup.sh