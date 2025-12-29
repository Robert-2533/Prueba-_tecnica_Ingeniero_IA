# Usamos la imagen oficial de Ollama
FROM ollama/ollama:latest

# Exponemos el puerto estándar
EXPOSE 11434

# Seteamos variables de entorno si es necesario
ENV OLLAMA_HOST=0.0.0.0

# Truco para descargar el modelo durante la construcción de la imagen:
# Levantamos el servidor en segundo plano, descargamos el modelo y luego cerramos el servidor.
RUN nohup bash -c "ollama serve &" && \
    sleep 5 && \
    ollama pull qwen2.5:1.5b

# El comando por defecto al iniciar el contenedor será arrancar el servidor
ENTRYPOINT ["ollama", "serve"]

# todo: meter todo esto en el docker-compose ya que no hay logica de nada aca

