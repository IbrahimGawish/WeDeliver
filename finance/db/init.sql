CREATE DATABASE IF NOT EXISTS finance;
USE finance;

CREATE TABLE IF NOT EXISTS finance_data (
  ID INT NOT NULL AUTO_INCREMENT,
  invoice_id INT,
  customer_id INT,
  amount INT,
  PRIMARY KEY (ID)
);
