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

Run the following commands from the repository root directory, where the Docker Compose file is located.

Build and start the application:

```powershell
docker compose up -d --build
```

Check container status:

```powershell
docker compose ps
```

The application container should report `healthy`.

## 5. Access the Application

Open the following URL in a web browser:

http://localhost:8501

The Smart CRM dashboard should load successfully.

## 6. Verify Deployment

- Confirm the Docker container is running.
- Confirm container health status is `healthy`.
- Confirm dashboard is accessible at `http://localhost:8501`.
- Confirm required warehouse CSV files exist in `data/warehouse/`.
- Verify the dashboard displays the available customer segmentation data.
- If segmentation data is unavailable, check the warehouse files and pipeline execution status.

## 7. Stop and Restart the Application

Stop the application:

```powershell
docker compose down
```

Restart the application:

```powershell
docker compose up -d
```

## 8. Troubleshooting

### Container is unhealthy

Check container status:

```powershell
docker compose ps
```

Check application logs:

```powershell
docker compose logs --tail 50
```

### Port 8501 is already in use

Stop the application using port 8501 or change the port mapping in `docker-compose.yml`.

### Application cannot load data

Verify that the required warehouse CSV files exist in `data/warehouse/`.

If data is missing or invalid, check the pipeline execution status and data quality validation results.

### Docker is not running

Start Docker Desktop and wait until the Docker Engine is ready.

## 9. Deployment Limitations

- This deployment is intended for local demonstration and testing.
- Production authentication and authorization are not fully implemented.
- Customer data should not be exposed publicly without appropriate access controls.
- Production deployment requires additional security configuration.