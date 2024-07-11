# Nombre de la imagen Docker
IMAGE_NAME = socialnetwork-client

# Puerto en el que se ejecutará la aplicación Streamlit
PORT = 8501

# Directorio del proyecto en tu máquina local
PROJECT_DIR = $(shell pwd)

# Directorio de trabajo dentro del contenedor
CONTAINER_DIR = /app

# Comando para construir la imagen Docker
.PHONY: docker-build 
docker-build:
	docker build -t $(IMAGE_NAME) .

# Comando para ejecutar el contenedor Docker con volumen montado
.PHONY: docker-run 
docker-run:
	docker run -p $(PORT):$(PORT) \
		-v $(PROJECT_DIR):$(CONTAINER_DIR) \
		-e PYTHONPATH=$(CONTAINER_DIR) \
		$(IMAGE_NAME)
