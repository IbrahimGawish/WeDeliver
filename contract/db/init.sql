CREATE DATABASE IF NOT EXISTS contract;
USE contract;

CREATE TABLE IF NOT EXISTS contracts_data (
  ID INT NOT NULL AUTO_INCREMENT,
  customer_id INT,
  vehicle_id INT,
  lease_start_date timestamp ,
  lease_end_date timestamp ,
  price_per_day INT,
  PRIMARY KEY (ID)
);
