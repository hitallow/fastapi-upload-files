CREATE TABLE IF NOT EXISTS boleto (
  id VARCHAR(36) PRIMARY key,
  name VARCHAR(50),
  debitId VARCHAR(50),
  governmentId VARCHAR(50),
  email VARCHAR(50),
  debitAmount INT NOT NULL,
  dueDate INT NOT NULL
)