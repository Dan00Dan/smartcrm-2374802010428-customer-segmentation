# Smart CRM – Deployment Guide

## 1. System Requirements

- Operating System: Windows 10/11, Linux, or macOS
- Docker Desktop with Docker Compose
- Git
- Minimum 4 GB RAM recommended
- Internet connection for downloading Docker images and dependencies

## 2. Prerequisites

Install the following software:

- Docker Desktop: https://www.docker.com/products/docker-desktop/
- Git: https://git-scm.com/downloads

Verify installation:

```powershell
docker --version
docker compose version
git --version
```

## 3. Clone the Repository

```powershell
git clone https://github.com/Dan00Dan/smartcrm-2374802010428-customer-segmentation.git
cd smartcrm-2374802010428-customer-segmentation
```

## 4. Deploy with Docker Compose

Build and start the application:

```powershell
docker compose up -d --build
```

Check container status:

```powershell
docker compose ps
```

The container should report `healthy`.

## 5. Access the Application

Open the following URL in a web browser:

http://localhost:8501

The Smart CRM dashboard should load successfully.

## 6. Verify Deployment

- Confirm the Docker container is running.
- Confirm container health status is `healthy`.
- Confirm dashboard is accessible at `http://localhost:8501`.
- Confirm required warehouse CSV files exist in `data/warehouse/`.
- Confirm dashboard displays the available customer segmentation data.

## 7. Stop and Restart the Application

Stop the application:

```powershell
docker compose down
```

Restart:

```powershell
docker compose up -d
```

## 8. Troubleshooting

### Container is unhealthy

Check logs:

```powershell
docker compose logs --tail 50
```

### Port 8501 is already in use

Stop the application using port 8501 or change the port mapping in `docker-compose.yml`.

### Application cannot load data

Verify that the required warehouse CSV files exist in `data/warehouse/`.

### Docker is not running

Start Docker Desktop and wait until the Docker Engine is ready.

## 9. Deployment Limitations

- This deployment is intended for local demonstration and testing.
- Production authentication and authorization are not fully implemented.
- Customer data should not be exposed publicly without appropriate access controls.
- Production deployment requires additional security configuration.
