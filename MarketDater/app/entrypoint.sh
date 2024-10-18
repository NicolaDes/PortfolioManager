#!/bin/sh

# Log di debug
echo "Eseguendo entrypoint.sh"

# Attende che Kafka sia pronto
echo "Verifico Kafka..."
while ! nc -z kafka 9092; do   
  sleep 1
  echo "Aspetto Kafka..."
done

# Verifica Redis
echo "Verifico Redis..."
while ! nc -z redis 6379; do
  sleep 1
  echo "Aspetto Redis..."
done

# Avvia l'applicazione
echo "Kafka e Redis pronti. Avvio l'applicazione..."
java -jar /app/myapp.jar
