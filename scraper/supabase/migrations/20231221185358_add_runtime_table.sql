CREATE TABLE runtime (
  id SERIAL PRIMARY KEY,
  vendor_id INTEGER NOT NULL,
  start_time TIMESTAMP,
  end_time TIMESTAMP,
  CONSTRAINT fk_vendor FOREIGN KEY (vendor_id) REFERENCES vendor(id)
);