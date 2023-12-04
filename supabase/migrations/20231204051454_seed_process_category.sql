INSERT INTO public.process_category (name) VALUES
('Washed'),
('Natural'),
('Honey'),
('Experimental'),
('Unknown')
ON CONFLICT (name) DO NOTHING;