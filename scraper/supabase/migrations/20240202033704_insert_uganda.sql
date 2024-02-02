INSERT INTO country (name, continent_id) VALUES
('Uganda', (SELECT id FROM continent WHERE name = 'Africa'))
ON CONFLICT (name) DO NOTHING;