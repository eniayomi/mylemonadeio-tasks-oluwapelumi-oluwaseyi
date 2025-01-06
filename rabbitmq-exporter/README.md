# RabbitMQ Prometheus Exporter

A Prometheus exporter that collects metrics from RabbitMQ's HTTP API (Management Plugin) and exports them in Prometheus format.

## Metrics Exported

- `rabbitmq_individual_queue_messages{host,vhost,name}` - Total number of messages in queue
- `rabbitmq_individual_queue_messages_ready{host,vhost,name}` - Number of messages ready in queue
- `rabbitmq_individual_queue_messages_unacknowledged{host,vhost,name}` - Number of unacknowledged messages in queue

## Prerequisites

- Python 3.6+
- RabbitMQ server with Management Plugin enabled
- Access to RabbitMQ HTTP API (default port: 15672)

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The exporter uses the following environment variables:

- `RABBITMQ_HOST` - RabbitMQ server hostname (default: localhost)
- `RABBITMQ_USER` - RabbitMQ username (default: guest)
- `RABBITMQ_PASSWORD` - RabbitMQ password (default: guest)
- `RABBITMQ_MANAGEMENT_PORT` - RabbitMQ Management Plugin port (default: 15672)
- `EXPORTER_PORT` - Prometheus exporter port (default: 9419)
## Usage

1. Set the environment variables:

2. Run the exporter:
   ```bash
   python rabbitmq_exporter.py
   ```

The exporter will start on port 9419 by default if you don't specify the port in the .env file. Metrics will be available at `http://localhost:9419/metrics`.

## Prometheus Configuration

Add the following to your `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'rabbitmq'
    static_configs:
      - targets: ['localhost:9419']
``` 