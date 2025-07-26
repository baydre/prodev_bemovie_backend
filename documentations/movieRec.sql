CREATE TABLE "users" (
  "id" integer PRIMARY KEY,
  "username" varchar UNIQUE NOT NULL,
  "email" varchar UNIQUE NOT NULL,
  "password" varchar NOT NULL,
  "first_name" varchar,
  "last_name" varchar,
  "is_active" boolean DEFAULT true,
  "is_staff" boolean DEFAULT false,
  "date_joined" timestamp,
  "last_login" timestamp
);

CREATE TABLE "favorite_movies" (
  "id" integer PRIMARY KEY,
  "user_id" integer NOT NULL,
  "movie_id" integer NOT NULL,
  "title" varchar,
  "poster_path" varchar,
  "added_at" timestamp
);

COMMENT ON COLUMN "users"."password" IS 'Hashed password';

COMMENT ON COLUMN "favorite_movies"."movie_id" IS 'TMDb movie ID';

COMMENT ON COLUMN "favorite_movies"."title" IS 'Movie title from TMDb';

COMMENT ON COLUMN "favorite_movies"."poster_path" IS 'TMDb poster path';

ALTER TABLE "favorite_movies" ADD CONSTRAINT "user_favorites" FOREIGN KEY ("user_id") REFERENCES "users" ("id");
