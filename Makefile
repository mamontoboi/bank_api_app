# Phony targets
.PHONY: venv migrate image delete_image container restart_cont stop_cont delete_cont shell test status purge


# Create and activate virtual environment
venv:
	python3 -m venv venv && source venv/bin/activate


# Make all migrations
migrate:
	docker exec -it nbp_cont python nbp_api/manage.py makemigrations
	docker exec -it nbp_cont python nbp_api/manage.py migrate


# Build the Docker image
image:
	docker build -t nbp .


# Delete the Docker image
delete_image:
	docker rmi nbp:latest


# Create and run the container
container:
	docker run --name nbp_cont -dp 8000:8000 nbp


# Restart the Docker container
restart_cont:
	docker start nbp_cont


# Stop the Docker container
stop_cont:
	docker stop nbp_cont


# Delete the Docker container
delete_cont:
	docker rm nbp_cont


# To start the shell
shell:
	docker exec -it nbp_cont sh


# To test the app
test:
	cd nbp_api/ && python3 manage.py test


# View status of all running Docker containers
status:
	docker ps


# Remove all unused Docker containers and images
purge:
	docker system prune -a
