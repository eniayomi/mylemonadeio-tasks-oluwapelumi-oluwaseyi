#!/bin/bash

#update these variables to match your setup
CPU_THRESHOLD=80
CHECK_INTERVAL=60  # seconds
LOG_FILE="laravel_monitor.log"
SERVICE_NAME="laravel.service"  # Change this to match your Laravel service name

# Function to get current timestamp
timestamp() {
    date "+%Y-%m-%d %H:%M:%S"
}

# Function to log messages
log() {
    echo "$(timestamp) - $1" | tee -a "$LOG_FILE"
}

# Function to get CPU usage
get_cpu_usage() {
    # Get CPU usage using top command for Linux
    top -bn1 | grep "Cpu(s)" | awk '{print $2}'
}

# Function to restart Laravel service
restart_service() {
    log "WARNING: CPU usage has gone above (${1}%). Restarting $SERVICE_NAME..."
    sudo systemctl restart $SERVICE_NAME
    
    if [ $? -eq 0 ]; then
        log "INFO: Service restart successful"
    else
        log "ERROR: Failed to restart service"
    fi
}

# Main monitoring loop
log "INFO: Starting Laravel CPU monitoring service"

while true; do
    CPU_USAGE=$(get_cpu_usage)
    log "INFO: Current CPU Usage: ${CPU_USAGE}%"
    
    if (( $(echo "$CPU_USAGE > $CPU_THRESHOLD" | bc -l) )); then
        restart_service $CPU_USAGE
        # Wait for 5 minutes after restart before checking again
        sleep 300
    else
        sleep $CHECK_INTERVAL
    fi
done 