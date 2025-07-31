# ProDev BEMovie Recommendation Backend

This project provides a robust backend for a movie recommendation application, focusing on API development, performance optimization with caching, and comprehensive documentation.

## Overview

The backend offers APIs for retrieving trending and recommended movies from TMDb, user authentication via JWT, and the ability for users to save their favorite movies. It's designed with modularity, performance, and security in mind.

## Project Goals

-   **API Creation:** Develop endpoints for fetching trending and recommended movies.
-   **User Management:** Implement user authentication and the ability to save favorite movies.
-   **Performance Optimization:** Enhance API performance with caching mechanisms.
-   **Comprehensive Documentation:** Use Swagger for API documentation.

## Technologies Used

-   **Django:** For backend development.
-   **Django REST Framework (DRF):** For building RESTful APIs.
-   **PostgreSQL:** Relational database for data storage.
-   **Redis:** Caching system for performance optimization.
-   **djangorestframework-simplejwt:** For JWT-based user authentication.
-   **drf-spectacular:** For API documentation (Swagger/OpenAPI).
-   **requests:** For interacting with the TMDb API.
-   **python-dotenv:** For managing environment variables.
-   **dj-database-url:** For parsing database URLs in settings.
-   **Docker & Docker Compose:** For containerization and orchestration.

## Project Structure

The backend is organized into three Django applications:

-   `users`: Manages user authentication and profiles.
-   `movies_data`: Handles external TMDb API interactions and public movie data.
-   `user_preferences`: Manages user-specific favorite movie data.
