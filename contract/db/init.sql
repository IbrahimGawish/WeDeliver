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

INSERT INTO contracts_data (customer_id, vehicle_id, lease_start_date,lease_end_date,price_per_day)
VALUES
(1, 1, '2023-11-01 12:00:00','2023-12-28 12:00:00',10),
(1, 1, '2023-11-01 12:00:00','2023-12-20 12:00:00',5),
(2, 3, '2022-11-01 12:00:00','2022-12-28 12:00:00',5),
(3, 4, '2022-11-01 12:00:00','2023-11-25 12:00:00',12);