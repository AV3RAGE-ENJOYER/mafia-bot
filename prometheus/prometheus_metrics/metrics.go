package prometheus_metrics

import "github.com/prometheus/client_golang/prometheus"

type Metrics struct {
	Users      prometheus.Gauge
	DailyUsers prometheus.Gauge
}

func NewMetrics(reg prometheus.Registerer) *Metrics {
	m := &Metrics{
		Users: prometheus.NewGauge(prometheus.GaugeOpts{
			Namespace: "app",
			Name:      "users",
			Help:      "Total number of users",
		}),
		DailyUsers: prometheus.NewGauge(prometheus.GaugeOpts{
			Namespace: "app",
			Name:      "daily_users",
			Help:      "Number of daily users",
		}),
	}
	reg.MustRegister(m.Users, m.DailyUsers)
	return m
}
