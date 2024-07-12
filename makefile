# Docker image name
IMAGE_NAME = socialnetwork-client

# Port on which the Streamlit application will run
PORT = 8501

# Project directory on your local machine
PROJECT_DIR = $(shell pwd)

# Working directory inside the container
CONTAINER_DIR = /app

# Python interpreter (use 'python' or 'python3' as appropriate for your system)
PYTHON = python3

# Virtual environment directory
VENV_DIR = venv

# --------------------------------------------------- Docker commands ---------------------------------------------------

# Command to build the Docker image
.PHONY: docker-build 
docker-build:
	docker build -t $(IMAGE_NAME) .

# Command to run the Docker container with mounted volume
.PHONY: docker-run 
docker-run:
	docker run -p $(PORT):$(PORT) \
		-v $(PROJECT_DIR):$(CONTAINER_DIR) \
		-e PYTHONPATH=$(CONTAINER_DIR) \
		$(IMAGE_NAME)

# --------------------------------------------------- Local commands ---------------------------------------------------

# Command to set up the virtual environment
.PHONY: venv
venv:
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/pip install -r requirements.txt

# Command to run the application
.PHONY: run
run: venv
	export PYTHONPATH=$(PROJECT_DIR) && \
	$(VENV_DIR)/bin/streamlit run app.py

# Command to clean up the virtual environment
.PHONY: clean
clean:
	rm -rf $(VENV_DIR)