-- Altering the data type of start_time to timestamptz
ALTER TABLE runtime
ALTER COLUMN start_time TYPE timestamptz USING start_time AT TIME ZONE 'UTC';

-- Altering the data type of end_time to timestamptz
ALTER TABLE runtime
ALTER COLUMN end_time TYPE timestamptz USING end_time AT TIME ZONE 'UTC';
