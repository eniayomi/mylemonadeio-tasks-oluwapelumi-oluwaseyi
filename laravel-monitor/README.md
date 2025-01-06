# Laravel CPU Monitor

A Bash script that monitors CPU usage and automatically restarts your Laravel service if CPU usage exceeds 80%.

## Prerequisites
- Laravel application configured as a systemd service
- `sudo` access (required for service restart)

## Configuration
Open `monitor_laravel.sh` and adjust these variables if needed:
```bash
CPU_THRESHOLD=80           # CPU threshold percentage
CHECK_INTERVAL=60         # Check interval in seconds
SERVICE_NAME="laravel.service"  # Your Laravel systemd service name
```

## Setting up Laravel as a systemd Service
Before using this script, ensure your Laravel application is configured as a systemd service. Example configuration:

1. Create a systemd service file:
```bash
sudo nano /etc/systemd/system/laravel.service
```

2. Add this configuration (adjust paths accordingly):
```ini
[Unit]
Description=Laravel Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/laravel
ExecStart=/usr/bin/php artisan serve
Restart=always

[Install]
WantedBy=multi-user.target
```

3. Enable and start the service:
```bash
sudo systemctl enable laravel.service
sudo systemctl start laravel.service
```

## Usage

1. Make the monitoring script executable:
```bash
chmod +x monitor_laravel.sh
```

2. Run the script:
```bash
sudo ./monitor_laravel.sh
```

The script will:
- Monitor CPU usage every 60 seconds
- Restart the Laravel service if CPU usage exceeds 80%
- Log all activities to `laravel_monitor.log`

## Monitor Logs
```bash
tail -f laravel_monitor.log
```

## Running as a Background Service

To run in the background:
```bash
nohup sudo ./monitor_laravel.sh > /dev/null 2>&1 &
```

To stop the service:
```bash
pkill -f "monitor_laravel.sh"
``` 