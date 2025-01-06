import os
import time
import requests
from dotenv import load_dotenv
from prometheus_client import start_http_server, Gauge
from typing import Dict, List

# Load environment variables from .env file
load_dotenv()

# Define Prometheus metrics
QUEUE_MESSAGES = Gauge('rabbitmq_individual_queue_messages',
                      'Total number of messages in queue',
                      ['host', 'vhost', 'name'])

QUEUE_MESSAGES_READY = Gauge('rabbitmq_individual_queue_messages_ready',
                            'Number of messages ready in queue',
                            ['host', 'vhost', 'name'])

QUEUE_MESSAGES_UNACK = Gauge('rabbitmq_individual_queue_messages_unacknowledged',
                            'Number of unacknowledged messages in queue',
                            ['host', 'vhost', 'name'])

class RabbitMQExporter:
    def __init__(self):
        self.host = os.getenv('RABBITMQ_HOST', 'localhost')
        self.user = os.getenv('RABBITMQ_USER', 'guest')
        self.password = os.getenv('RABBITMQ_PASSWORD', 'guest')
        # RabbitMQ Management Plugin uses port 15672 by default
        self.management_port = os.getenv('RABBITMQ_MANAGEMENT_PORT', '15672')
        self.base_url = f'{self.host}:{self.management_port}/api'
        self.session = requests.Session()
        self.session.auth = (self.user, self.password)

    def get_queue_metrics(self) -> List[Dict]:
        """Fetch metrics for all queues in all vhosts."""
        try:
            response = self.session.get(f'{self.base_url}/queues')
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching queue metrics: {e}")
            return []

    def update_metrics(self):
        """Update Prometheus metrics with current RabbitMQ queue data."""
        queues = self.get_queue_metrics()
        
        for queue in queues:
            labels = {
                'host': self.host,
                'vhost': queue['vhost'],
                'name': queue['name']
            }
            
            QUEUE_MESSAGES.labels(**labels).set(queue['messages'])
            QUEUE_MESSAGES_READY.labels(**labels).set(queue['messages_ready'])
            QUEUE_MESSAGES_UNACK.labels(**labels).set(queue['messages_unacknowledged'])

def main():
    # Get exporter port from environment variables
    exporter_port = int(os.getenv('EXPORTER_PORT', '9419'))
    
    # Start Prometheus HTTP server
    start_http_server(exporter_port)
    print(f"Prometheus metrics server started on port {exporter_port}")
    
    exporter = RabbitMQExporter()
    
    # Update metrics every 15 seconds
    while True:
        try:
            exporter.update_metrics()
        except Exception as e:
            print(f"Error updating metrics: {e}")
        time.sleep(15)

if __name__ == '__main__':
    main() 