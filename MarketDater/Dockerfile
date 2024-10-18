# Stage 1: Build
FROM maven:3.8.1-openjdk-11-slim AS builder

# Imposta la directory di lavoro per la build
WORKDIR /app

# Copia pom.xml separatamente
COPY app/pom.xml .

# Scarica le dipendenze Maven
RUN mvn dependency:go-offline

# Copia tutto il contenuto della cartella app
COPY app .

# Costruisci il progetto Maven senza eseguire i test
RUN mvn clean package -DskipTests

# Stage 2: Runtime
FROM openjdk:11-jre-slim

# Installa netcat
RUN apt-get update && apt-get install -y netcat

# Imposta la directory di lavoro
WORKDIR /app

# Copia l'applicazione costruita dallo stage builder
COPY --from=builder /app/target/myapp-1.0.0.jar /app/myapp.jar

# Espone la porta 8000 per la tua applicazione
EXPOSE 8000

# Copia e imposta lo script di entrypoint
COPY app/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Comando di esecuzione
CMD ["sh", "/app/entrypoint.sh"]
