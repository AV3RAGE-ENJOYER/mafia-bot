FROM golang:latest
WORKDIR /usr/share/mafia_app_migrations/
COPY . .
RUN go mod download && go mod verify
RUN go build migrate.go
CMD ["./migrate"]