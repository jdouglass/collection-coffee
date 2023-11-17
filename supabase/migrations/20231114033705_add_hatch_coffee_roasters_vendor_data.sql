INSERT INTO vendor (name, currency_code_id, country_id) VALUES
('Hatch Coffee Roasters', (SELECT id FROM currency_code WHERE code = 'CAD'), (SELECT id FROM country WHERE name = 'Canada'))
ON CONFLICT (name) DO NOTHING;