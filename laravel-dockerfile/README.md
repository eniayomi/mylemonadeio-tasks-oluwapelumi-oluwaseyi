# Laravel Production Docker Setup

A production-ready Docker setup for Laravel applications with Nginx, PHP-FPM, and Supervisor.

## Features

- PHP 8.2-FPM
- Nginx web server
- Supervisor for process management
- Common PHP extensions pre-installed
- Latest Composer
- Proper user permissions setup
- Process monitoring for PHP-FPM and Nginx

## Prerequisites

- Docker installed on your system
- A Laravel application

## Usage

1. Copy these files to your Laravel project root:
   - `Dockerfile`
   - `supervisord.conf`
   - `.dockerignore`

2. Build the Docker image:
```bash
docker build -t your-app-name .
```

3. Run the container:
```bash
docker run -d \
    -p 80:80 \
    --name your-app \
    your-app-name
```

## Included PHP Extensions

- GD
- PDO
- PDO MySQL
- Sockets

## Configuration

### Supervisor
The setup includes Supervisor to manage:
- PHP-FPM process
- Nginx process

All logs are redirected to stdout/stderr for proper Docker logging.

### User Configuration
The container runs with a default user 'laravel' with UID 1000, which has the necessary permissions to run the application.

## License
MIT 