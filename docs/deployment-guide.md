# Smart CRM – Deployment Guide

## 1. Requirements

### System Requirements

- Windows 10/11, Linux, or macOS
- Docker Desktop with Docker Compose
- Git
- Minimum 4 GB RAM recommended
- Internet connection for downloading Docker images and dependencies

### Required Software

- Docker Desktop: https://www.docker.com/products/docker-desktop/
- Git: https://git-scm.com/downloads

Verify installation:

```powershell
docker --version
docker compose version
git --version
```

## 2. Setup

### Clone the Repository

```powershell
git clone https://github.com/Dan00Dan/smartcrm-2374802010428-customer-segmentation.git
cd smartcrm-2374802010428-customer-segmentation
```

### Configure Environment

Create a local environment file:

```powershell
Copy-Item .env.example .env
```

Review `.env` and configure the required values if applicable.

### Start the Application

```powershell
docker compose up -d --build
```

Check container status:

```powershell
docker compose ps
```

The application container should report `healthy`.

## 3. Environment Variables

Environment configuration is managed through the `.env` file.

- `.env.example` provides the configuration template.
- `.env` contains local environment-specific values.
- Do not commit `.env` or real credentials to GitHub.
- Update environment values according to the local deployment requirements.

If no additional environment variables are required, retain the default values provided by the project configuration.

## 4. Sample Data

The repository may not contain real customer data because customer information must be protected.

Before running the data pipeline:

- Prepare the required customer and order datasets in the expected local data directories.
- Use approved sample or synthetic data for demonstrations.
- Do not upload real customer information, phone numbers, or sensitive records to a public repository.
- Verify that the required input files match the expected data structure.

The dashboard can only display the data that has been successfully processed and loaded into the warehouse.

## 5. Verify Deployment

### Application Verification

Open the application:

http://localhost:8501

Verify the following:

- Docker container is running.
- Container health status is `healthy`.
- Dashboard is accessible.
- Required warehouse files exist in `data/warehouse/`.
- Dashboard displays available customer segmentation data.
- Data quality results are displayed correctly.

### Pipeline Verification

Run the data processing pipeline when the required input datasets are available:

```powershell
python -m src.pipeline
```

Run warehouse loading:

```powershell
docker compose exec smartcrm python -m src.etl.load_warehouse
```

Check the pipeline output and warehouse data quality results before interpreting segmentation results.

### Stop and Restart

Stop the application:

```powershell
docker compose down
```

Restart:

```powershell
docker compose up -d
```

## 6. Troubleshooting

### Container is unhealthy

```powershell
docker compose ps
docker compose logs --tail 50
```

### Port 8501 is already in use

Stop the application using port 8501 or modify the port mapping in `docker-compose.yml`.

### Application cannot load data

- Verify required warehouse files exist.
- Check pipeline execution status.
- Review data quality validation results.
- Confirm the input datasets match the expected schema.

### Docker is not running

Start Docker Desktop and wait until Docker Engine is ready.

## 7. Deployment Limitations

- This deployment is intended for local demonstration and testing.
- Production authentication and authorization are not fully implemented.
- Real customer data must not be exposed publicly without appropriate access controls.
- Production deployment requires additional security configuration.
- A clean repository clone does not automatically include private customer datasets.
- Demonstration data should be synthetic or appropriately anonymized.