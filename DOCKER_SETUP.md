# Docker Setup Guide

This guide explains how to run the BeMovie Backend application using Docker and Docker Compose.

## Prerequisites

- Docker 20.10 or later
- Docker Compose 2.0 or later

## Quick Start

1. **Clone the repository** (if not already done):
   ```bash
   git clone <your-repo-url>
   cd prodev_bemovie_backend
   ```

2. **Copy environment variables**:
   ```bash
   cp .env.example .env
   ```

3. **Update the `.env` file** with your specific configuration:
   - Change `DJANGO_SECRET_KEY` to a secure random key
   - Update database credentials if needed
   - Set your domain in `DJANGO_ALLOWED_HOSTS` for production

4. **Build and run the services**:
   ```bash
   # For development (includes auto-reload)
   docker-compose up --build

   # For production (with nginx)
   docker-compose --profile production up --build
   ```

## Services

### Development Environment
- **Django Web App**: `http://localhost:8000`
- **PostgreSQL**: `localhost:5432`
- **Redis**: `localhost:6379`

### Production Environment
- **Nginx (Frontend)**: `http://localhost:80`
- **Django Web App**: `http://localhost:8000` (internal)
- **PostgreSQL**: `localhost:5432`
- **Redis**: `localhost:6379`

## Docker Compose Commands

### Basic Operations
```bash
# Start all services
docker-compose up

# Start services in background
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f web

# Rebuild services
docker-compose up --build
```

### Database Operations
```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access database shell
docker-compose exec db psql -U bemovie_user -d bemovie_db

# Backup database
docker-compose exec db pg_dump -U bemovie_user bemovie_db > backup.sql
```

### Django Management Commands
```bash
# Collect static files
docker-compose exec web python manage.py collectstatic

# Run Django shell
docker-compose exec web python manage.py shell

# Run tests
docker-compose exec web python manage.py test

# Check deployment readiness
docker-compose exec web python manage.py check --deploy
```

### Development Tools
```bash
# Install new dependencies (regenerate uv.lock)
uv add <package-name>
docker-compose up --build web

# Access container shell
docker-compose exec web bash

# View container logs
docker-compose logs -f web
```

## File Structure

```
.
├── Dockerfile              # Main application container
├── docker-compose.yaml     # Production services definition
├── docker-compose.override.yaml  # Development overrides
├── entrypoint.sh           # Container startup script
├── nginx.conf             # Nginx configuration
├── .env.example           # Environment variables template
├── pyproject.toml         # Python dependencies (uv)
├── uv.lock               # Locked dependencies
└── DOCKER_SETUP.md       # This file
```

## Key Features

### Dockerfile Improvements
- **UV Package Manager**: Faster dependency resolution and installation
- **Multi-stage optimized**: Minimal production image
- **Security**: Non-root user, minimal attack surface
- **Health Checks**: Built-in application health monitoring

### Entrypoint Script
- **Database Wait**: Waits for PostgreSQL and Redis to be ready
- **Auto-migrations**: Runs database migrations on startup
- **Static Files**: Collects static files automatically
- **Superuser Creation**: Optional automated superuser setup

### Docker Compose Features
- **Health Checks**: Services wait for dependencies to be healthy
- **Persistent Data**: Database and Redis data persist across restarts
- **Development Override**: Auto-reload and source code mounting for development
- **Production Profile**: Includes Nginx reverse proxy
- **Network Isolation**: Services communicate through dedicated network

## Environment Variables

Key environment variables (see `.env.example` for complete list):

| Variable | Description | Default |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Django secret key | Required |
| `DJANGO_DEBUG` | Enable debug mode | `False` |
| `DATABASE_URL` | PostgreSQL connection string | `postgres://...` |
| `REDIS_URL` | Redis connection string | `redis://...` |
| `DJANGO_SUPERUSER_*` | Auto-create superuser | Optional |

## Troubleshooting

### Common Issues

1. **Port conflicts**: Change port mappings in `docker-compose.yaml`
2. **Permission errors**: Ensure Docker has proper permissions
3. **Database connection**: Check if PostgreSQL is healthy: `docker-compose ps`
4. **Static files**: Run `docker-compose exec web python manage.py collectstatic`

### Reset Everything
```bash
# Stop and remove all containers, networks, and volumes
docker-compose down -v --remove-orphans

# Remove images (optional)
docker-compose down --rmi all

# Start fresh
docker-compose up --build
```

## Production Deployment

For production deployment:

1. Update environment variables in `.env`
2. Use production profile: `docker-compose --profile production up -d`
3. Set up SSL termination (recommend using a reverse proxy like Traefik or external load balancer)
4. Configure proper backup strategies for PostgreSQL
5. Monitor logs and metrics
6. Use Docker Swarm or Kubernetes for multi-node deployments

## Security Considerations

- Change default passwords and secret keys
- Use environment-specific `.env` files
- Enable SSL/TLS in production
- Regularly update base images
- Monitor container security with tools like Docker Scout
- Use secrets management for sensitive data
