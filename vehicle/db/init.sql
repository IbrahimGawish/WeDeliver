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
INSERT INTO vehicles_data (vehicle_type, vehicle_status, rent_price)
VALUES
('Car', 'Active', 10),
('Motorcycle', 'Active', 5);
