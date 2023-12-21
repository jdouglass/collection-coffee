CREATE OR REPLACE function public.handle_new_user()
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.profiles (id, first_name, last_name)
  VALUES (
    new.id, 
    new.raw_user_meta_data->>'firstName', 
    new.raw_user_meta_data->>'lastName');
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY definer;