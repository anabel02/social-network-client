# social-network-client

# social-network-distributed-system

| **Nombre**              | **Grupo** | **Github**                                     |
|-------------------------|-----------|------------------------------------------------|
| Anabel Benítez González | C411      | [@anabel02](https://github.com/anabel02)       |
| Raudel Gómez Molina     | C411      | [@raudel25](https://github.com/raudel25)   |      



## Descripción
Este proyecto busca crear una plataforma de comunicación descentralizada, inspirada en Twitter pero con un enfoque en la privacidad y la resistencia a fallos. Este sistema permite a los usuarios compartir mensajes cortos, seguir a otros y republicar contenido, todo ello en una arquitectura distribuida que garantiza la escalabilidad geográfica y la tolerancia a desconexiones.

## ¿Cómo ejecutarlo?
1. Clona el repositorio
2. Navega al directorio del proyecto:
   ```bash
   cd social-network-distributed-system
   ```
Claro, aquí tienes las instrucciones separadas para ejecutar el proyecto con y sin Docker:

### Docker:

1. Asegúrate de tener Docker instalado en tu sistema.

3. Construye la imagen Docker:
   ```
   make docker-build
   ```

4. Para ejecutar el contenedor Docker:
   ```
   make docker-run
   ```
   Esto iniciará la aplicación en el puerto 8501 por defecto.

5. Si deseas ejecutar múltiples instancias con diferentes IDs, usa:
   ```
   make docker-run ID=1
   ```
   Esto iniciará la aplicación en el puerto 8502, y así sucesivamente.

### Local:

1. Asegúrate de tener Python instalado en tu sistema.

3. Crea y activa el entorno virtual:
   ```
   make venv
   source venv/bin/activate
   ```

4. Ejecuta la aplicación:
   ```
   make run
   ```

5. Para generar los archivos de protocolo gRPC (si es necesario):
   ```
   make proto
   ```

6. Para limpiar el entorno virtual cuando hayas terminado:
   ```
   make clean
   ```

En ambos casos, la aplicación estará disponible en `http://localhost:<PUERTO>` después de ejecutarla. El puerto por defecto es 8501.