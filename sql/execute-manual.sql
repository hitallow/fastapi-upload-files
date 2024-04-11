CREATE DATABASE IF NOT EXISTS kanastra;
-- create table to handle migrations
CREATE TABLE migrations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  fileName varchar(50),
  executedAt INT DEFAULT CURRENT_TIMESTAMP
)