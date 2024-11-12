package main

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"prometheus-metrics/prometheus_metrics"
	"strconv"
	"time"

	"github.com/IBM/sarama"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
	"github.com/redis/go-redis/v9"
)

type UserCount struct {
	BotType string `json:"bot_type"`
	Value   int    `json:"user_count"`
}

type DailyUser struct {
	BotType string `json:"bot_type"`
	Value   int    `json:"daily_users"`
}

func ConnectConsumer(brokers []string) (sarama.Consumer, error) {
	config := sarama.NewConfig()
	config.Consumer.Return.Errors = true

	return sarama.NewConsumer(brokers, config)
}

var usersTopic string = "users"
var dailyUsersTopic string = "daily_users"

func main() {
	rdb := redis.NewClient(&redis.Options{
		Addr:     "redis-server:6379",
		Password: "", // no password set
		DB:       0,  // use default DB
	})

	// REDIS INIT

	userCountString, err := rdb.Get(context.Background(), "user_count").Result()
	if err != nil {
		log.Fatalf(" [ERROR] Failed to get user count. %s", err)
	}

	userCount, _ := strconv.Atoi(userCountString)

	dailyUsers, err := rdb.SMembers(context.Background(), "daily_users").Result()
	if err != nil {
		log.Fatalf(" [ERROR] Failed to get daily users. %s", err)
	}

	// PROMETHEUS INIT

	reg := prometheus.NewRegistry()
	m := prometheus_metrics.NewMetrics(reg)

	m.Users.Set(float64(userCount))
	m.DailyUsers.Set(float64(len(dailyUsers)))

	prometheusMux := http.NewServeMux()
	prometheusMux.Handle("/metrics", promhttp.HandlerFor(reg, promhttp.HandlerOpts{}))

	// KAFKA INIT

	worker, err := ConnectConsumer([]string{"kafka:29092"})

	if err != nil {
		log.Fatalf(" [ERROR] Failed to connect to kafka. %s", err)
	}

	defer worker.Close()

	consumerUsers, err := worker.ConsumePartition(usersTopic, 0, sarama.OffsetNewest)

	if err != nil {
		log.Fatalf(" [ERROR] Failed to consume partition. %s", err)
	}

	consumerDailyUsers, err := worker.ConsumePartition(dailyUsersTopic, 0, sarama.OffsetNewest)

	if err != nil {
		log.Fatalf(" [ERROR] Failed to consume partition. %s", err)
	}

	// STARTING GOROUTINES

	log.Println("Prometheus metrics started")

	go func() {
		log.Fatal(http.ListenAndServe(":8081", prometheusMux))
	}()

	log.Println("Consumers started")

	go func() {
		for {
			select {
			case err := <-consumerUsers.Errors():
				log.Println(err)
			case msg := <-consumerUsers.Messages():
				var userCount UserCount

				err = json.Unmarshal(msg.Value, &userCount)

				if err != nil {
					log.Println(" [ERROR] Failed to decode json")
					continue
				}

				m.Users.Set(float64(userCount.Value))

				log.Printf("Received new User: Bot(%s) | Count(%d) | Topic(%s)\n",
					userCount.BotType,
					userCount.Value,
					string(msg.Topic))
			}
		}
	}()

	go func() {
		for {
			select {
			case err := <-consumerDailyUsers.Errors():
				log.Println(err)
			case msg := <-consumerDailyUsers.Messages():
				var dailyUser DailyUser

				err = json.Unmarshal(msg.Value, &dailyUser)

				if err != nil {
					log.Println(" [ERROR] Failed to decode json")
					continue
				}

				m.DailyUsers.Set(float64(dailyUser.Value))

				log.Printf("Received new Daily User: Bot(%s) | User(%d) | Topic(%s)\n",
					dailyUser.BotType,
					dailyUser.Value,
					string(msg.Topic))
			}
		}
	}()

	go func() {
		day := time.Now().Day()

		for {
			t := time.Now()
			n := time.Date(t.Year(), t.Month(), day+1, 0, 0, 0, 0, t.Location())

			if t.After(n) {
				dailyUsers, err := rdb.SMembers(context.Background(), "daily_users").Result()
				if err != nil {
					log.Fatalf(" [ERROR] Failed to get daily users. %s", err)
				}

				rdb.SPopN(context.Background(), "daily_users", int64(len(dailyUsers))).Result()

				m.DailyUsers.Set(0)

				day = t.Day()

				log.Println(" [INFO] Updated daily users list.")
			}

			time.Sleep(1 * time.Minute)
		}
	}()

	select {}
}
