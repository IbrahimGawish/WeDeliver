CREATE DATABASE IF NOT EXISTS vehicles;
USE vehicles;

CREATE TABLE IF NOT EXISTS vehicles_data (
  ID INT NOT NULL AUTO_INCREMENT,
  vehicle_type VARCHAR(50),
  vehicle_status VARCHAR(50),
  onboard_date TIMESTAMP,
  rent_price INT,
  PRIMARY KEY (ID)
);

-- Insert some initial data
INSERT INTO vehicles_data (vehicle_type, vehicle_status, rent_price,onboard_date)
VALUES
('Car', 'Leased', 10,'2023-12-28 12:00:00'),
('Motorcycle', 'Leased', 5,'2023-12-20 12:00:00'),
('Motorcycle', 'Active', 5,'2022-12-28 12:00:00'),
('Car', 'Leased', 12,'2023-11-28 12:00:00');
