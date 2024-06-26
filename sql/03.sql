CREATE TABLE IF NOT EXISTS fileImport (
  id VARCHAR(36) PRIMARY KEY,
  title VARCHAR(50),
  status VARCHAR(20) NOT NULL,
  createdAt INT DEFAULT CURRENT_TIMESTAMP,
  updatedAt INT DEFAULT CURRENT_TIMESTAMP,
  fileId VARCHAR(36),
  FOREIGN KEY (fileId) REFERENCES file(id)
)