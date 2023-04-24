# Define phony targets
.PHONY: build start restart stop shell test status purge migrate collectstatic cretesuperuser runserver

# Build the Docker image
build:
	docker build -t nbp .

# Create and run the container
start:
	docker run --name nbp_cont -dp 8000:8000 nbp

# Restart the Docker container
restart:
	docker start nbp_cont

# To start the shell
shell:
	docker exec -it nbp_cont sh

# To test the app
test:
	cd nbp_api/ && python3 manage.py test

# Stop the Docker container
stop:
	docker stop nbp_cont

# View status of all running Docker containers
status:
	docker ps

# Remove all unused Docker containers and images
purge:
	docker system prune -a

# Make all migrations
migrate:
	docker exec -it nbp_cont python manage.py makemigrations
	docker exec -it nbp_cont python manage.py migrate

# Collect static files
collectstatic:
	docker exec -it nbp_cont python manage.py collectstatic

# Create super cretesuperuser
cretesuperuser:
	docker exec -it nbp_cont python manage.py createsuperuser

# Run Django app
runserver:
	docker exec -it nbp_cont python manage.py runserver