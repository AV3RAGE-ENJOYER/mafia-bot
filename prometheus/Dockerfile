FROM golang:latest
WORKDIR /usr/share/mafia_prometheus_metrics/
COPY . .
RUN go mod download && go mod verify
RUN go build kafka-consumer.go
CMD ["./kafka-consumer"]