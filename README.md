# ProDev BEMovie Recommendation Backend

This project provides a robust backend for a movie recommendation application. It covers API development, performance optimization with caching, and comprehensive documentation.

## Overview

The backend offers APIs for retrieving trending and recommended movies from TMDb, supports user authentication via JWT, and allows users to manage their favorite movies. Designed with modularity, performance, and security in mind, this project delivers a seamless movie discovery experience.

## Technologies Used

### Backend Framework
- **Django 5.2+** - High-level Python web framework for rapid development
- **Django REST Framework (DRF)** - Powerful toolkit for building Web APIs
- **Python 3.11+** - Modern Python with improved performance and type hints

### Database & Caching
- **PostgreSQL** - Advanced open-source relational database
- **Redis** - In-memory data structure store for caching and session management
- **django-redis** - Redis cache backend for Django

### Authentication & Security
- **djangorestframework-simplejwt** - JSON Web Token authentication for DRF
- **JWT (JSON Web Tokens)** - Secure token-based authentication
- **Django's built-in security features** - CSRF protection, SQL injection prevention

### API Documentation
- **drf-spectacular** - OpenAPI 3.0 schema generation for Django REST Framework
- **Swagger UI** - Interactive API documentation interface
- **OpenAPI 3.0** - Industry-standard API specification

### External Services
- **TMDb API** - The Movie Database API for movie data
- **requests** - HTTP library for API interactions

### Development & Package Management
- **uv** - Fast Python package installer and resolver
- **python-dotenv** - Environment variable management
- **dj-database-url** - Database URL parsing utility

### Testing
- **Django's testing framework** - Built-in testing capabilities
- **unittest.mock** - Mock object library for testing
- **APITestCase** - DRF's test case for API testing

### Deployment & Infrastructure
- **Docker** - Containerization platform
- **Docker Compose** - Multi-container Docker applications
- **Kubernetes** (Optional) - Container orchestration platform

### Code Quality & Standards
- **PEP 8** - Python style guide compliance
- **Type hints** - Static type checking support
- **Modular architecture** - Clean separation of concerns

## Setup Instructions

### Prerequisites
- Python 3.11+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) - Fast Python package installer
- Redis server
- PostgreSQL database

### Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/prodev_bemovie_backend.git
   cd prodev_bemovie_backend
   ```

2. **Install Dependencies with uv:**
   ```bash
   uv sync
   ```
   This will automatically create a virtual environment and install all dependencies from `pyproject.toml`.

3. **Activate Virtual Environment:**
   ```bash
   source .venv/bin/activate
   ```

4. **Environment Variables:**
   Create a `.env` file in the project root with the following variables:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=postgresql://username:password@localhost:5432/dbname
   TMDB_API_KEY=your-tmdb-api-key
   ```

5. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create Superuser (Optional):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start Development Server:**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

- **Auth:**
  - `POST /api/auth/register/`: Register a new user.
  - `POST /api/token/`: Obtain JWT token.
  - `GET /api/auth/profile/`: User profile management.

- **Movies:**
  - `GET /api/movies/trending/`: Get trending movies.
  - `GET /api/movies/{id}/`: Get movie details.
  - `GET /api/movies/{id}/recommendations/`: Get movie recommendations.
  - `GET /api/movies/search/?q=title`: Search movies by title.

- **Favorites:**
  - `GET /api/favourites/`: List user favorites.
  - `POST /api/favourites/`: Add a favorite movie.
  - `DELETE /api/favourites/{id}/`: Remove a favorite movie.

## Documentation

Interactive API documentation is available via Swagger UI:
- Visit `/api/docs/` after starting the server to explore and test endpoints.

## Development and Testing

### Running Tests

- **All Tests:**
  ```bash
  python manage.py test --settings=movie_rec_project.test_settings
  ```

- **Specific App Tests:**
  ```bash
  python manage.py test users --settings=movie_rec_project.test_settings
  python manage.py test movies --settings=movie_rec_project.test_settings
  python manage.py test favourites --settings=movie_rec_project.test_settings
  ```

- **Integration Tests:**
  ```bash
  python manage.py test integration_tests --settings=movie_rec_project.test_settings
  ```

### Development with uv

- **Add New Dependencies:**
  ```bash
  uv add package-name
  ```

- **Add Development Dependencies:**
  ```bash
  uv add --dev package-name
  ```

- **Update Dependencies:**
  ```bash
  uv sync
  ```

### Features
- **Comprehensive Test Coverage:** Unit tests, integration tests, and API protection tests
- **Redis Caching:** Movie data is cached to improve response times
- **JWT Authentication:** Secure user authentication and authorization
- **API Documentation:** Interactive Swagger documentation

## Docker Deployment

### Local Development with Docker

1. **Prerequisites:**
   - Docker and Docker Compose installed
   - Clone the repository

2. **Build and Run:**
   ```bash
   # Build the Docker image
   docker-compose build
   
   # Start all services (PostgreSQL, Redis, Django)
   docker-compose up
   ```

   This will start:
   - PostgreSQL database on port 5432
   - Redis cache on port 6379
   - Django application on port 8000

3. **Access the Application:**
   - API: http://localhost:8000/api/
   - Admin: http://localhost:8000/admin/
   - API Documentation: http://localhost:8000/api/docs/

### Production Deployment

#### Render.com Deployment

1. **Quick Deploy:**
   - Fork this repository
   - Connect your GitHub account to Render
   - Use the included `render.yaml` for automatic setup

2. **Manual Setup:**
   - Create a new web service on Render
   - Connect your GitHub repository
   - Set environment to "Docker"
   - Configure environment variables:
     ```
     SECRET_KEY=<generate-random-secret>
     DEBUG=False
     ALLOWED_HOSTS=your-app-name.onrender.com
     DATABASE_URL=<render-postgres-url>
     REDIS_URL=<render-redis-url>
     TMDB_API_KEY=<your-tmdb-api-key>
     ```
   - Deploy!

#### Other Platforms

- **Heroku:** Use the Dockerfile for container deployment
- **DigitalOcean App Platform:** Docker-based deployment supported
- **AWS/GCP/Azure:** Use container services with the provided Docker configuration

## Evaluation Criteria

- **Functionality:** Full API coverage with robust error-handling.
- **Performance:** Optimized queries and caching to enhance response times.
- **Security:** JWT authentication safeguards APIs and user data.
- **Documentation:** Clear API documentation and setup guidelines for ease of use.

## Project Structure

The backend is organized into three Django applications:

-   `users`: Manages user authentication and profiles.
-   `movies`: Handles external TMDb API interactions and public movie data.
-   `favourites`: Manages user-specific favorite movie data.
