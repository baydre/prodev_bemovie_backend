# Movie Recommendation App Backend: Entity-Relationship Diagram (ERD) Design

This section describes the entities and their relationships for the PostgreSQL database used in the Movie Recommendation App backend. Django's ORM will manage these models.

## Entities:
### 1. User (Managed by Django's built-in auth.User model)
**Attributes**:
`id` (Primary Key, Integer)
`username` (String, Unique)
`email` (String, Unique)
`password` (String, Hashed)
first_name (String, Optional)
last_name (String, Optional)
is_active (Boolean)
is_staff (Boolean)
date_joined (Timestamp)
last_login (Timestamp, Nullable)
Purpose: Stores user authentication details and basic profile information.

### 2. FavoriteMovie
**Attributes**:
id (Primary Key, Integer)
user_id (Foreign Key to User.id, Integer)
movie_id (Integer, TMDb movie ID)
title (String, e.g., "The Shawshank Redemption")
poster_path (String, TMDb poster path, Nullable)
added_at (Timestamp, Auto-generated on creation)
Purpose: Stores a user's favorite movies, linking to the User model and storing relevant movie metadata from TMDb.

### 3. Constraints:
`user_id` and `movie_id` together form a unique constraint (a user can favorite a specific movie only once).
**Relationships**:
- User to FavoriteMovie (One-to-Many):
    - A `User` can have multiple `FavoriteMovie` entries.
    - Each `FavoriteMovie` entry belongs to exactly one `User`.
    - This relationship is established by the `user_id` foreign key in the `FavoriteMovie` table, referencing the id of the `User` table.
    - **Relationship Type**: One-to-Many

Simplified ERD Representation (Textual): image

ERD Visual (dbdiagram.io): image

**Notes on Data Storage**:
- Movie Data: Detailed movie information (genres, runtime, etc.) is not stored directly in the database. It is fetched on-demand from the TMDb API. Only essential metadata for favorite movies (ID, title, poster path) is stored to minimize database size and ensure data consistency with the external API.
- Caching: Redis will be used for caching TMDb API responses, not for persistent storage of movie details.
- User Preferences: The `FavoriteMovie` table is designed to store user-specific preferences efficiently.
