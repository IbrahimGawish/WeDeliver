CREATE DATABASE IF NOT EXISTS customer;
USE customer;

CREATE TABLE IF NOT EXISTS customers_data (
  ID INT NOT NULL AUTO_INCREMENT,
  customer_name VARCHAR(250),
  customer_n_leased INT unsigned DEFAULT 0,
  customer_balance INT unsigned DEFAULT 0,
  PRIMARY KEY (ID)
);

-- Insert some initial data
INSERT INTO customers_data (customer_name)
VALUES
('customer_1'),
('customer_2');
