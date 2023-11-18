INSERT INTO vendor (name, currency_code_id, country_id) VALUES
('Black Creek Coffee', (SELECT id FROM currency_code WHERE code = 'CAD'), (SELECT id FROM country WHERE name = 'Canada')),
('Continuum Coffee Roasters', (SELECT id FROM currency_code WHERE code = 'CAD'), (SELECT id FROM country WHERE name = 'Canada')),
('De Mello', (SELECT id FROM currency_code WHERE code = 'CAD'), (SELECT id FROM country WHERE name = 'Canada')),
('Heart Coffee Roasters', (SELECT id FROM currency_code WHERE code = 'CAD'), (SELECT id FROM country WHERE name = 'Canada')),
('House of Funk Brewing', (SELECT id FROM currency_code WHERE code = 'CAD'), (SELECT id FROM country WHERE name = 'Canada')),
('Library Specialty Coffee', (SELECT id FROM currency_code WHERE code = 'CAD'), (SELECT id FROM country WHERE name = 'Canada')),
('Luna Coffee', (SELECT id FROM currency_code WHERE code = 'CAD'), (SELECT id FROM country WHERE name = 'Canada')),
('Matchstick', (SELECT id FROM currency_code WHERE code = 'CAD'), (SELECT id FROM country WHERE name = 'Canada')),
('Monogram Coffee', (SELECT id FROM currency_code WHERE code = 'CAD'), (SELECT id FROM country WHERE name = 'Canada')),
('Nemesis Coffee', (SELECT id FROM currency_code WHERE code = 'CAD'), (SELECT id FROM country WHERE name = 'Canada')),
('Pallet Coffee Roasters', (SELECT id FROM currency_code WHERE code = 'CAD'), (SELECT id FROM country WHERE name = 'Canada')),
('Phil & Sebastian', (SELECT id FROM currency_code WHERE code = 'CAD'), (SELECT id FROM country WHERE name = 'Canada')),
('Pirates of Coffee', (SELECT id FROM currency_code WHERE code = 'CAD'), (SELECT id FROM country WHERE name = 'Canada')),
('Prairie Lily Coffee', (SELECT id FROM currency_code WHERE code = 'CAD'), (SELECT id FROM country WHERE name = 'Canada')),
('Quietly Coffee', (SELECT id FROM currency_code WHERE code = 'CAD'), (SELECT id FROM country WHERE name = 'Canada')),
('Rabbit Hole Roasters', (SELECT id FROM currency_code WHERE code = 'CAD'), (SELECT id FROM country WHERE name = 'Canada')),
('Rosso Coffee', (SELECT id FROM currency_code WHERE code = 'CAD'), (SELECT id FROM country WHERE name = 'Canada')),
('Sam James Coffee Bar', (SELECT id FROM currency_code WHERE code = 'CAD'), (SELECT id FROM country WHERE name = 'Canada')),
('September Coffee', (SELECT id FROM currency_code WHERE code = 'CAD'), (SELECT id FROM country WHERE name = 'Canada')),
('Sey Coffee', (SELECT id FROM currency_code WHERE code = 'USD'), (SELECT id FROM country WHERE name = 'United States')),
('Sorellina Coffee', (SELECT id FROM currency_code WHERE code = 'CAD'), (SELECT id FROM country WHERE name = 'Canada')),
('Subtext Coffee Roasters', (SELECT id FROM currency_code WHERE code = 'CAD'), (SELECT id FROM country WHERE name = 'Canada')),
('The Angry Roaster', (SELECT id FROM currency_code WHERE code = 'CAD'), (SELECT id FROM country WHERE name = 'Canada')),
('Thom Bargen Coffee Roasters', (SELECT id FROM currency_code WHERE code = 'CAD'), (SELECT id FROM country WHERE name = 'Canada')),
('Transcend Coffee', (SELECT id FROM currency_code WHERE code = 'CAD'), (SELECT id FROM country WHERE name = 'Canada')),
('Zab Café', (SELECT id FROM currency_code WHERE code = 'CAD'), (SELECT id FROM country WHERE name = 'Canada'))
ON CONFLICT (name) DO NOTHING;