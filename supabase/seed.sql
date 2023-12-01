-- Seed the `product_type` table
INSERT INTO product_type (name) VALUES
('Roasted Whole Bean'),
('Green Whole Bean'),
('Instant'),
('Capsule'),
('Unknown')
ON CONFLICT (name) DO NOTHING;

-- Seed the `process_category` table
INSERT INTO process_category (name) VALUES
('Washed'),
('Natural'),
('Honey'),
('Experimental'),
('Unknown')
ON CONFLICT (name) DO NOTHING;

-- Seed the vendor table
INSERT INTO vendor (name, currency_code_id, country_id) VALUES
('Traffic Coffee', (SELECT id FROM currency_code WHERE code = 'CAD'), (SELECT id FROM country WHERE name = 'Canada')),
('Eight Ounce Coffee', (SELECT id FROM currency_code WHERE code = 'CAD'), (SELECT id FROM country WHERE name = 'Canada')),
('Revolver Coffee', (SELECT id FROM currency_code WHERE code = 'CAD'), (SELECT id FROM country WHERE name = 'Canada'))
ON CONFLICT (name) DO NOTHING;
