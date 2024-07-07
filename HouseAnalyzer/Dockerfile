FROM golang:1.22
WORKDIR /app
COPY /app/ .

RUN go mod tidy
RUN go build -o /godocker