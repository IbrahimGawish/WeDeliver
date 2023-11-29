CREATE DATABASE IF NOT EXISTS customer;
USE customer;

CREATE TABLE IF NOT EXISTS customers_data (
  ID INT NOT NULL AUTO_INCREMENT,
  customer_name VARCHAR(250),
  customer_n_leased INT unsigned DEFAULT 0,
  customer_balance INT  DEFAULT 0,
  PRIMARY KEY (ID)
);

INSERT INTO customers_data (customer_name,customer_n_leased)
VALUES
('customer_1',2),
('customer_2',0),
('customer_3',1);
