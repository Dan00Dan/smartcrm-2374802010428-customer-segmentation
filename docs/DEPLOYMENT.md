# Smart CRM - Deployment Guide

## 1. System Requirements

- Operating System: Windows 10/11, Linux, or macOS
- Docker Desktop with Docker Compose
- Internet connection for downloading Docker images and dependencies
- Minimum 4 GB RAM recommended

## 2. Prerequisites

Install the following software:

- Docker Desktop: https://www.docker.com/products/docker-desktop/
- Git: https://git-scm.com/downloads

Verify installation:

```bash
docker --version
docker compose version
git --version
```

## 3. Clone the Repository

```bash
git clone https://github.com/Dan00Dan/smartcrm-2374802010428-customer-segmentation.git
cd smartcrm-2374802010428-customer-segmentation
```

## 4. Environment Configuration

Create the environment file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Review `.env` and configure the required environment variables.

Do not commit `.env` to Git.

## 5. Deploy with Docker

Build the Docker image:

```bash
docker compose build
```

Start the application:

```bash
docker compose up -d
```

Check container status:

```bash
docker compose ps
```

The container should report a healthy status.

## 6. Access the Application

Open the following URL in a web browser:

http://localhost:8501

The Smart CRM dashboard should load successfully.

## 7. Stop the Application

```bash
docker compose down
```

To restart:

```bash
docker compose up -d
```

## 8. Troubleshooting

### Container is unhealthy

Check logs:

```bash
docker compose logs --tail 50
```

### Port 8501 is already in use

Stop the application using port 8501 or change the port mapping in `docker-compose.yml`.

### Application cannot load data

Verify that the required warehouse CSV files exist in `data/warehouse/`.

### Docker is not running

Start Docker Desktop and wait until the Docker Engine is ready.