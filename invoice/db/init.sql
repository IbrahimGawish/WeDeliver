CREATE DATABASE IF NOT EXISTS invoice;
USE invoice;

CREATE TABLE IF NOT EXISTS invoices_data (
  ID INT NOT NULL AUTO_INCREMENT,
  invoice_payment_status VARCHAR(50),
  invoice_amount INT unsigned DEFAULT 0,
  customer_id INT,
  PRIMARY KEY (ID)
);
-- Insert some initial data
-- INSERT INTO invoices_data (invoice_payment_status,invoice_amount)
-- VALUES
-- ('UnPaid',100),
-- ('PartiallyPaid',100),
-- ('FullyPaid',100);
