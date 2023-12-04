INSERT INTO public.product_type (name) VALUES
('Roasted Whole Bean'),
('Green Whole Bean'),
('Instant'),
('Capsule'),
('Unknown')
ON CONFLICT (name) DO NOTHING;