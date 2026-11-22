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

Create a local environment file from the provided template:

```powershell
Copy-Item .env.example .env
```

Generate a secure pseudonymization secret with at least 32 characters:

```powershell
$secret = python -c "import secrets; print(secrets.token_hex(32))"
(Get-Content .env) -replace '^CRM_PSEUDONYM_SECRET=.*$', "CRM_PSEUDONYM_SECRET=$secret" | Set-Content -Encoding UTF8 .env
```

The generated secret is used to pseudonymize customer identifiers during warehouse loading.

Review `.env` and configure other environment variables according to the local deployment requirements.

**Security requirements:**

- Keep the actual `.env` file private.
- Never commit `.env` or real credentials to GitHub.
- Do not share the pseudonymization secret publicly.
- Keep the same secret when continuing to use an existing warehouse dataset, because changing it may produce different pseudonymized customer identifiers.

### Start the Application

Build and start the application using Docker Compose:

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

| Variable | Description | Requirement |
|---|---|---|
| `DB_HOST` | Database server address | Depends on database configuration |
| `DB_PORT` | Database connection port | Depends on database configuration |
| `DB_NAME` | Database name | Depends on database configuration |
| `DB_USER` | Database username | Depends on database configuration |
| `DB_PASSWORD` | Database password | Depends on database configuration |
| `APP_PORT` | Application port configuration | Template default: 3000 |
| `SECRET_KEY` | Application security key | Configure when required |
| `CRM_PSEUDONYM_SECRET` | Secret used for customer pseudonymization | Required; minimum 32 characters |

### Required Pseudonymization Secret

- `CRM_PSEUDONYM_SECRET` is required when loading customer data into the warehouse.
- The secret must contain at least 32 characters.
- Generate a secure random secret for each new deployment environment.
- Keep the secret unchanged when continuing to use an existing warehouse dataset.
- Store the secret securely and never commit it to Git.

Additional notes:

- `.env.example` provides the configuration template.
- `.env` contains local environment-specific values.
- `.env` is excluded from version control.
- Do not use real customer credentials or sensitive information in public configuration files.

## 4. Sample Data

The repository may not contain real customer data because customer information must be protected.

Before running the data pipeline:

- Prepare the required customer and order datasets in the expected local data directories.
- Use approved sample or synthetic data for demonstrations.
- Do not upload real customer information, phone numbers, or sensitive records to a public repository.
- Verify that the required input files match the expected data structure.

The dashboard can only display the data that has been successfully processed and loaded into the warehouse.

For Docker deployment, the local warehouse directory is mounted into the container as a read-only volume:

```yaml
volumes:
  - ./data/warehouse:/app/data/warehouse:ro
```

Therefore, the required warehouse files must exist locally before the dashboard can display the corresponding data.

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

Run the data processing pipeline when the required input datasets are available and the local Python environment has the necessary dependencies installed:

```powershell
python -m src.pipeline
```

Run warehouse loading when the required environment variables and input data are available:

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

Check the container status:

```powershell
docker compose ps
```

View application logs:

```powershell
docker compose logs --tail 50
```

### Port 8501 is already in use

Stop the application using port 8501 or modify the port mapping in `docker-compose.yml`.

### Application cannot load data

- Verify required warehouse files exist.
- Check pipeline execution status.
- Review data quality validation results.
- Confirm the input datasets match the expected schema.
- Verify that the warehouse directory is correctly mounted into the container.

### Missing CRM_PSEUDONYM_SECRET

If warehouse loading reports that `CRM_PSEUDONYM_SECRET` is missing or too short:

- Check that `.env` contains the `CRM_PSEUDONYM_SECRET` variable.
- Ensure its value has at least 32 characters.
- Restart the container after changing environment variables:

```powershell
docker compose down
docker compose up -d
```

### Docker is not running

Start Docker Desktop and wait until Docker Engine is ready.

## 7. Deployment Limitations

- This deployment is intended for local demonstration and testing.
- Production authentication and authorization are not fully implemented.
- Real customer data must not be exposed publicly without appropriate access controls.
- Production deployment requires additional security configuration.
- A clean repository clone does not automatically include private customer datasets.
- Demonstration data should be synthetic or appropriately anonymized.
- Customer pseudonymization depends on securely managing `CRM_PSEUDONYM_SECRET`.
- Changing the pseudonymization secret may change generated customer identifiers and affect consistency with previously generated warehouse data.