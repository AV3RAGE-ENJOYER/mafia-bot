package main

import (
	"context"
	"log"
	"os"

	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/jackc/pgx/v5/stdlib"
	"github.com/joho/godotenv"
	"github.com/pressly/goose"
)

type PostgresDB struct {
	Pool *pgxpool.Pool
}

func NewDB(ctx context.Context, DB_URL string) (PostgresDB, error) {
	dbPool, err := pgxpool.New(ctx, DB_URL)

	if err != nil {
		return PostgresDB{}, err
	}

	postgres := PostgresDB{dbPool}
	return postgres, nil
}

func main() {
	godotenv.Load("config.env")

	MAGFIA_DB_URL := os.Getenv("MAGFIA_DB_URL")
	MINEFIA_DB_URL := os.Getenv("MINEFIA_DB_URL")

	DATABASE_NAMES := []string{"magfia", "minefia"}

	DB_URLS := []string{MAGFIA_DB_URL, MINEFIA_DB_URL}

	for i, DB_URL := range DB_URLS {
		db, err := NewDB(context.Background(), DB_URL)

		if err != nil {
			log.Fatalf(" [Error] Failed to establish a connection to PostgresDB. %s", err)
		}

		defer db.Pool.Close()

		if err := goose.SetDialect("postgres"); err != nil {
			log.Fatalf(" [Error] %s\n", err)
		}

		driver := stdlib.OpenDBFromPool(db.Pool)

		log.Printf(" [Info] Migrating database %s", DATABASE_NAMES[i])

		if err := goose.Up(driver, "sql_migrations"); err != nil {
			log.Fatalf(" [Error] %s\n", err)
		}

		if err := driver.Close(); err != nil {
			log.Fatalf(" [Error] %s", err)
		}
	}

	log.Println("[INFO] Migrations ran successfully")
}
