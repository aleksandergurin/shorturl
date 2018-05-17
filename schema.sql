-- Database schema

CREATE TABLE IF NOT EXISTS short_url (
  id  BIGSERIAL PRIMARY KEY,
  url TEXT UNIQUE NOT NULL
);

